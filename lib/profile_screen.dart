import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({Key? key}) : super(key: key);

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  String _selectedSignLanguage = 'ASL';
  String? _temporaryUiLanguage; 

  final List<String> _allDropdownLanguages = [
    'English',
    'Bahasa Melayu',
    'Bahasa Indonesia',
    '中文 (Chinese)',
    'ភាសាខ្មែរ (Khmer)',
    'ພາສາລາວ (Lao)',
    'မြန်မာ (Burmese)',
    'Tagalog',
    'ภาษาไทย (Thai)',
    'Tiếng Việt (Vietnamese)',
  ];

  final Map<String, String> _functionalLanguages = {
    'English': 'en',
    'Bahasa Melayu': 'ms',
    'Bahasa Indonesia': 'id',
    '中文 (Chinese)': 'zh',
  };

  @override
  Widget build(BuildContext context) {
    String currentLocaleCode = context.locale.languageCode;
    
    String activeFunctionalName = _functionalLanguages.entries
        .firstWhere((entry) => entry.value == currentLocaleCode, orElse: () => const MapEntry('English', 'en'))
        .key;

    String displayLanguage = _temporaryUiLanguage ?? activeFunctionalName;

    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.only(top: 60, bottom: 30, left: 24, right: 24),
              decoration: const BoxDecoration(
                color: Color(0xFF009688),
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(30),
                  bottomRight: Radius.circular(30),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'profile_title'.tr(),
                    style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 24),
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(color: Colors.white.withOpacity(0.2)),
                    ),
                    child: Column(
                      children: [
                        Row(
                          children: [
                            const CircleAvatar(
                              radius: 30,
                              backgroundColor: Color(0xFF00695C),
                              child: Text('KL', style: TextStyle(color: Colors.white, fontSize: 20)),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text(
                                    'Kelvin Law Yun Hong',
                                    style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                                  ),
                                  Text(
                                    'learning_status'.tr(),
                                    style: const TextStyle(color: Colors.white70, fontSize: 14),
                                  ),
                                ],
                              ),
                            )
                          ],
                        ),
                        const Padding(
                          padding: EdgeInsets.symmetric(vertical: 16.0),
                          child: Divider(color: Colors.white30),
                        ),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: [
                            _buildStatItem('150', 'cards_mastered'.tr()),
                            _buildStatItem('24', 'day_streak'.tr()),
                            _buildStatItem('89%', 'accuracy'.tr()),
                          ],
                        )
                      ],
                    ),
                  )
                ],
              ),
            ),
            
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  _buildSettingsCard(
                    title: 'language_settings'.tr(),
                    icon: Icons.language,
                    iconColor: Colors.teal,
                    iconBg: Colors.teal.shade50,
                    content: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('app_interface_language'.tr(), style: const TextStyle(color: Colors.black87)),
                        const SizedBox(height: 8),
                        _buildInterfaceLanguageDropdown(displayLanguage), 
                        
                        const SizedBox(height: 16),
                        Text('target_sign_language'.tr(), style: const TextStyle(color: Colors.black87)),
                        const SizedBox(height: 8),
                        _buildTargetSignLanguageDropdown(),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),
                  
                  _buildSettingsCard(
                    title: 'accessibility'.tr(),
                    icon: Icons.shield_outlined,
                    iconColor: Colors.purple,
                    iconBg: Colors.purple.shade50,
                    content: Column(
                      children: [
                        SwitchListTile(
                          contentPadding: EdgeInsets.zero,
                          title: Text('sound_feedback'.tr(), style: const TextStyle(fontWeight: FontWeight.w500)),
                          subtitle: Text('sound_subtitle'.tr(), style: const TextStyle(fontSize: 12)),
                          value: true,
                          activeColor: const Color(0xFF009688),
                          onChanged: (bool value) {},
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatItem(String value, String label) {
    return Column(
      children: [
        Text(value, style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
        const SizedBox(height: 4),
        Text(label, textAlign: TextAlign.center, style: const TextStyle(color: Colors.white70, fontSize: 12)),
      ],
    );
  }

  Widget _buildSettingsCard({required String title, required IconData icon, required Color iconColor, required Color iconBg, required Widget content}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 10, offset: const Offset(0, 4))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(color: iconBg, shape: BoxShape.circle),
                child: Icon(icon, color: iconColor, size: 20),
              ),
              const SizedBox(width: 12),
              Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 20),
          content,
        ],
      ),
    );
  }

  Widget _buildInterfaceLanguageDropdown(String currentValue) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: currentValue,
          isExpanded: true,
          icon: const Icon(Icons.keyboard_arrow_down, color: Colors.grey),

          items: _allDropdownLanguages.map((String lang) {
            return DropdownMenuItem<String>(
              value: lang,
              child: Text(lang, style: const TextStyle(fontWeight: FontWeight.w500)),
            );
          }).toList(),
          onChanged: (String? newValue) {
            if (newValue != null) {
              
              if (_functionalLanguages.containsKey(newValue)) {
                setState(() {
                  _temporaryUiLanguage = null; 
                });
                String newLocaleCode = _functionalLanguages[newValue]!;
                context.setLocale(Locale(newLocaleCode)); 

                setState(() {
                  _temporaryUiLanguage = newValue; 
                });
                
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Translation for $newValue is coming soon!'),
                    backgroundColor: Colors.orange.shade800,
                    behavior: SnackBarBehavior.floating,
                    duration: const Duration(seconds: 3),
                  ),
                );
              }
            }
          },
        ),
      ),
    );
  }

  Widget _buildTargetSignLanguageDropdown() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: _selectedSignLanguage,
          isExpanded: true,
          icon: const Icon(Icons.keyboard_arrow_down, color: Colors.grey),
          items: ['ASL', 'BIM', 'BISINDO', 'SgSL'].map((String lang) {
            return DropdownMenuItem<String>(
              value: lang,
              child: Text(lang, style: const TextStyle(fontWeight: FontWeight.w500)),
            );
          }).toList(),
          onChanged: (String? newValue) {
            if (newValue != null) {
              setState(() {
                _selectedSignLanguage = newValue;
              });
            }
          },
        ),
      ),
    );
  }
}