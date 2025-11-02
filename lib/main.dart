import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:just_audio/just_audio.dart';
import 'pages/audio_detail_page.dart'; // make sure this file exists

void main() => runApp(MyApp());

class MyApp extends StatefulWidget {
  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final player = AudioPlayer();
  List<dynamic> audioList = [];
  bool isLoading = true;
  int? currentIndex;

  // Your IPv4 address
  String IPV4_Adress = "192.168.137.1";

  @override
  void initState() {
    super.initState();
    fetchAudioData();
  }

  Future<void> fetchAudioData() async {
    try {
      final response = await http
          .get(Uri.parse('http://$IPV4_Adress:5000/api/audio'))
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        // ✅ Print only audio_file_path for each item
        for (var item in data) {
          print("AUDIO FILE PATH: ${item['audio_file_path']}");
        }

        setState(() {
          audioList = data;
          isLoading = false;
        });
      } else {
        throw Exception('Failed to load data');
      }
    } catch (e) {
      print('Error fetching audio data: $e');
      setState(() => isLoading = false);
    }
  }


  Future<void> togglePlayPause(String url, int index) async {
    try {
      if (currentIndex == index && player.playing) {
        await player.pause();
      } else {
        await player.setUrl(url);
        await player.play();
        setState(() {
          currentIndex = index;
        });
      }
    } catch (e) {
      print('Error playing audio: $e');
    }
  }

  String formatTime(Duration d) {
    String twoDigits(int n) => n.toString().padLeft(2, '0');
    final minutes = twoDigits(d.inMinutes.remainder(60));
    final seconds = twoDigits(d.inSeconds.remainder(60));
    return "$minutes:$seconds";
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(title: const Text('VoxPulse JustAudio Player')),
        body: isLoading
            ? const Center(child: CircularProgressIndicator())
            : StreamBuilder<PlayerState>(
          stream: player.playerStateStream,
          builder: (context, snapshot) {
            final state = snapshot.data;
            final playing = state?.playing ?? false;

            return ListView.builder(
              itemCount: audioList.length,
              itemBuilder: (context, index) {
                final item = audioList[index];
                final isThisPlaying = currentIndex == index && playing;

                return Card(
                  margin: const EdgeInsets.all(8),
                  child: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Column(
                      children: [
                        ListTile(
                          title: Text(item['title']),
                          subtitle: Text(item['category'] ?? ''),
                          onTap: () {
                            // Navigate to the detail page
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => AudioDetailPage(
                                  item: item,
                                  ipv4Address: IPV4_Adress,
                                ),
                              ),
                            );
                          },
                          trailing: IconButton(
                            icon: Icon(
                              isThisPlaying
                                  ? Icons.pause
                                  : Icons.play_arrow,
                              color: Colors.blue,
                            ),
                            onPressed: () => togglePlayPause(
                                item['audio_file_path'], index),
                          ),
                        ),
                        if (isThisPlaying)
                          StreamBuilder<Duration>(
                            stream: player.positionStream,
                            builder: (context, posSnapshot) {
                              final position =
                                  posSnapshot.data ?? Duration.zero;
                              final total =
                                  player.duration ?? Duration.zero;
                              return Column(
                                children: [
                                  Slider(
                                    min: 0,
                                    max: total.inSeconds.toDouble(),
                                    value: position.inSeconds
                                        .clamp(0, total.inSeconds)
                                        .toDouble(),
                                    onChanged: (v) {
                                      player.seek(
                                          Duration(seconds: v.toInt()));
                                    },
                                  ),
                                  Row(
                                    mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                    children: [
                                      Text(formatTime(position)),
                                      Text(formatTime(total)),
                                    ],
                                  ),
                                ],
                              );
                            },
                          ),
                      ],
                    ),
                  ),
                );
              },
            );
          },
        ),
      ),
    );
  }
}
