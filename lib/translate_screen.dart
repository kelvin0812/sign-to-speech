import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart'; // Add this

class TranslateScreen extends StatefulWidget {
  const TranslateScreen({Key? key}) : super(key: key);

  @override
  State<TranslateScreen> createState() => _TranslateScreenState();
}

class _TranslateScreenState extends State<TranslateScreen> {
  String _translatedText = 'Hello, how are you today?';

  void _clearText() {
    setState(() {
      _translatedText = '';
    });
  }

  void _triggerTextToSpeech() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('camera_prompt_snackbar'.tr()), // Translated!
        backgroundColor: const Color(0xFF009688),
        duration: const Duration(seconds: 3),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // Camera Feed Section
          Expanded(
            flex: 6,
            child: Container(
              width: double.infinity,
              decoration: const BoxDecoration(
                color: Color(0xFF1E293B),
                borderRadius: BorderRadius.only(bottomLeft: Radius.circular(24), bottomRight: Radius.circular(24)),
              ),
              child: SafeArea(
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    Positioned(
                      top: 16,
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        decoration: BoxDecoration(color: const Color(0xFF009688), borderRadius: BorderRadius.circular(20)),
                        child: Row(
                          children: [
                            const Icon(Icons.circle, color: Colors.white, size: 10),
                            const SizedBox(width: 8),
                            Text('detecting_signs'.tr(), style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                          ],
                        ),
                      ),
                    ),
                    Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text('camera_feed'.tr(), style: const TextStyle(color: Colors.white54, fontSize: 18)),
                        const SizedBox(height: 8),
                        Text('detection_active'.tr(), style: const TextStyle(color: Colors.white38, fontSize: 14)),
                      ],
                    ),
                    _buildCornerBracket(top: 40, left: 24, angle: 0),
                    _buildCornerBracket(top: 40, right: 24, angle: 1.57),
                    _buildCornerBracket(bottom: 40, right: 24, angle: 3.14),
                    _buildCornerBracket(bottom: 40, left: 24, angle: -1.57),
                  ],
                ),
              ),
            ),
          ),
          
          // Output Section
          Expanded(
            flex: 4,
            child: Container(
              padding: const EdgeInsets.all(24.0),
              color: Colors.white,
              child: Container(
                padding: const EdgeInsets.all(24.0),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 20, offset: const Offset(0, 5))],
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('translated_text'.tr(), style: const TextStyle(color: Colors.grey, fontSize: 14)),
                        TextButton.icon(
                          onPressed: _clearText,
                          icon: const Icon(Icons.close, size: 16, color: Colors.grey),
                          label: Text('clear_btn'.tr(), style: const TextStyle(color: Colors.grey)),
                        )
                      ],
                    ),
                    Text(
                      _translatedText.isEmpty ? 'waiting_signs'.tr() : _translatedText,
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 24, 
                        fontWeight: FontWeight.w500,
                        color: _translatedText.isEmpty ? Colors.grey : Colors.black
                      ),
                    ),
                    SizedBox(
                      width: double.infinity,
                      height: 54,
                      child: ElevatedButton.icon(
                        onPressed: _triggerTextToSpeech,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF009688),
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                        ),
                        icon: const Icon(Icons.volume_up),
                        label: Text('play_tts'.tr(), style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCornerBracket({double? top, double? bottom, double? left, double? right, required double angle}) {
    return Positioned(
      top: top, bottom: bottom, left: left, right: right,
      child: Transform.rotate(
        angle: angle,
        child: Container(
          width: 40, height: 40,
          decoration: const BoxDecoration(
            border: Border(top: BorderSide(color: Color(0xFF00E5FF), width: 3), left: BorderSide(color: Color(0xFF00E5FF), width: 3)),
            borderRadius: BorderRadius.only(topLeft: Radius.circular(12)),
          ),
        ),
      ),
    );
  }
}