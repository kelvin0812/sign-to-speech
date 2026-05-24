import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart'; // Add this
import 'sign_data.dart';

class StudyScreen extends StatefulWidget {
  const StudyScreen({Key? key}) : super(key: key);

  @override
  State<StudyScreen> createState() => _StudyScreenState();
}

class _StudyScreenState extends State<StudyScreen> {
  late List<SignItem> _flashcards;
  int _currentIndex = 0;
  bool _isFlipped = false;

  @override
  void initState() {
    super.initState();
    _flashcards = List.from(allSigns)..shuffle();
  }

  void _flipCard() {
    setState(() {
      _isFlipped = !_isFlipped;
    });
  }

  void _nextCard() {
    if (_currentIndex < _flashcards.length - 1) {
      setState(() {
        _currentIndex++;
        _isFlipped = false;
      });
    }
  }

  void _prevCard() {
    if (_currentIndex > 0) {
      setState(() {
        _currentIndex--;
        _isFlipped = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    SignItem currentSign = _flashcards[_currentIndex];
    double progress = (_currentIndex + 1) / _flashcards.length;

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('study_title'.tr(), style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              const SizedBox(height: 20),
              
              // Progress Bar
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('progress_label'.tr(), style: const TextStyle(color: Colors.grey)),
                        Text('${_currentIndex + 1} / ${_flashcards.length} ${'cards_count'.tr()}', 
                          style: TextStyle(color: Theme.of(context).primaryColor, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    const SizedBox(height: 10),
                    LinearProgressIndicator(
                      value: progress,
                      backgroundColor: Colors.grey.shade200,
                      valueColor: AlwaysStoppedAnimation<Color>(Theme.of(context).primaryColor),
                      borderRadius: BorderRadius.circular(10),
                      minHeight: 8,
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              
              // Main Flashcard
              Expanded(
                child: GestureDetector(
                  onTap: _flipCard,
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 300),
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: _isFlipped ? const Color(0xFFE0F2F1) : Colors.white,
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 20, offset: const Offset(0, 5))],
                    ),
                    child: Center(
                      child: _isFlipped 
                        ? Text(
                            currentSign.word, 
                            style: const TextStyle(fontSize: 48, fontWeight: FontWeight.bold, color: Color(0xFF00695C))
                          )
                        : Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text('category_${currentSign.category.toLowerCase()}'.tr(), style: const TextStyle(color: Colors.grey, fontSize: 16)),
                              const SizedBox(height: 20),
                              SizedBox(
                                height: 150,
                                width: 150,
                                child: Image.asset(
                                  currentSign.imagePath,
                                  errorBuilder: (context, error, stackTrace) => const Icon(Icons.image, size: 80, color: Colors.black26),
                                ),
                              ),
                              const SizedBox(height: 20),
                              Text('tap_to_reveal'.tr(), style: const TextStyle(color: Colors.grey, fontStyle: FontStyle.italic)),
                            ],
                          ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 24),
              
              // Actions
              SizedBox(
                width: double.infinity,
                height: 54,
                child: OutlinedButton.icon(
                  onPressed: _flipCard,
                  icon: const Icon(Icons.refresh),
                  label: Text('flip_to_see'.tr(), style: const TextStyle(fontSize: 16)),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Theme.of(context).primaryColor,
                    side: BorderSide(color: Theme.of(context).primaryColor),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              
              Row(
                children: [
                  Expanded(
                    child: SizedBox(
                      height: 54,
                      child: ElevatedButton.icon(
                        onPressed: _currentIndex > 0 ? _prevCard : null,
                        icon: const Icon(Icons.chevron_left),
                        label: Text('btn_previous'.tr()),
                        style: ElevatedButton.styleFrom(
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: SizedBox(
                      height: 54,
                      child: ElevatedButton(
                        onPressed: _currentIndex < _flashcards.length - 1 ? _nextCard : null,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Theme.of(context).primaryColor,
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text('btn_next'.tr(), style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                            const SizedBox(width: 8),
                            const Icon(Icons.chevron_right),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              
              Center(
                child: Padding(
                  padding: const EdgeInsets.only(top: 16.0, bottom: 4.0),
                  child: Text(
                    'image_credits'.tr(),
                    style: TextStyle(color: Colors.grey.shade500, fontSize: 12, fontStyle: FontStyle.italic),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}