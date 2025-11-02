import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';
import 'package:url_launcher/url_launcher.dart';

class AudioDetailPage extends StatefulWidget {
  final dynamic item;
  final String ipv4Address;

  const AudioDetailPage({
    Key? key,
    required this.item,
    required this.ipv4Address,
  }) : super(key: key);

  @override
  State<AudioDetailPage> createState() => _AudioDetailPageState();
}

class _AudioDetailPageState extends State<AudioDetailPage> {
  late AudioPlayer _player;
  bool isPlaying = false;
  Duration position = Duration.zero;
  Duration duration = Duration.zero;

  @override
  void initState() {
    super.initState();
    _player = AudioPlayer();

    _initializeAudio(); // ✅ use the direct URL

    _player.positionStream.listen((p) {
      setState(() => position = p);
    });

    _player.durationStream.listen((d) {
      setState(() => duration = d ?? Duration.zero);
    });
  }

  Future<void> _initializeAudio() async {
    try {
      await _player.setUrl(widget.item['audio_file_path']);
    } catch (e) {
      print('Error setting audio URL: $e');
    }
  }

  Future<void> _togglePlayPause() async {
    if (_player.playing) {
      await _player.pause();
      setState(() {
        isPlaying = false;
      });
    } else {
      await _player.play();
      setState(() {
        isPlaying = true;
      });
    }
  }


  Future<void> _launchURL(String url) async {
    final Uri uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Could not open the link")),
      );
    }
  }

  String _formatTime(Duration d) {
    String twoDigits(int n) => n.toString().padLeft(2, '0');
    final minutes = twoDigits(d.inMinutes.remainder(60));
    final seconds = twoDigits(d.inSeconds.remainder(60));
    return "$minutes:$seconds";
  }

  @override
  void dispose() {
    _player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final item = widget.item;

    return Scaffold(
      appBar: AppBar(
        title: Text(item['title']),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            // Summary section
            Text(
              "Summary",
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),

            Card(
              elevation: 3,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Container(
                constraints: const BoxConstraints(
                  maxHeight: 450, // limit visible height
                ),
                padding: const EdgeInsets.all(12),
                child: SingleChildScrollView(
                  child: Text(
                    item['content_text'] ?? "No summary available.",
                    style: const TextStyle(fontSize: 16, height: 1.4),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Audio controls
            Center(
              child: Column(
                children: [
                  // Progress slider ABOVE the controls
                  Slider(
                    min: 0,
                    max: duration.inSeconds.toDouble(),
                    value: position.inSeconds.clamp(0, duration.inSeconds).toDouble(),
                    onChanged: (v) async {
                      await _player.seek(Duration(seconds: v.toInt()));
                    },
                  ),

                  // Time display
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(_formatTime(position)),
                      Text(_formatTime(duration)),
                    ],
                  ),

                  const SizedBox(height: 10),

                  // Rectangular play/pause button
                  SizedBox(
                    width: 180,
                    height: 56,
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      onPressed: _togglePlayPause,
                      icon: Icon(
                        isPlaying ? Icons.pause : Icons.play_arrow,
                        color: Colors.white,
                        size: 32,
                      ),
                      label: Text(
                        isPlaying ? "Pause" : "Play",
                        style: const TextStyle(
                          fontSize: 18,
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 30),

            // Reference Links section
            if (item['reference_links'] != null && item['reference_links'].toString().isNotEmpty)
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Reference Links",
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 8),

                  // Split links by comma or space
                  ...item['reference_links']
                      .toString()
                      .split(RegExp(r'[,\s]+'))
                      .where((link) => link.trim().isNotEmpty)
                      .map((link) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4.0),
                    child: TextButton(
                      onPressed: () => _launchURL(link.trim()),
                      child: Text(
                        link.trim(),
                        style: const TextStyle(
                          color: Colors.blue,
                          decoration: TextDecoration.underline,
                        ),
                      ),
                    ),
                  ))
                      .toList(),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
