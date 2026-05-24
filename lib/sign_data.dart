class SignItem {
  final String word;
  final String category;
  final String imagePath;

  SignItem({required this.word, required this.category, required this.imagePath});
}

final List<SignItem> allSigns = [
  SignItem(word: 'Hello', category: 'Greetings', imagePath: 'assets/greetings/hello.png'),
  SignItem(word: 'Thank You', category: 'Greetings', imagePath: 'assets/greetings/thank_you.png'),
  SignItem(word: 'Please', category: 'Greetings', imagePath: 'assets/greetings/please.png'),
  SignItem(word: 'Sorry', category: 'Greetings', imagePath: 'assets/greetings/sorry.png'),
  SignItem(word: 'Yes', category: 'Greetings', imagePath: 'assets/greetings/yes.png'),
  SignItem(word: 'No', category: 'Greetings', imagePath: 'assets/greetings/no.png'),
  
  ...List.generate(26, (index) {
    String letter = String.fromCharCode(65 + index);
    return SignItem(
        word: letter, 
        category: 'Alphabet', 
        imagePath: 'assets/alphabet/$letter.png' 
    );
  }),

  ...List.generate(10, (index) {
    int number = index + 1;
    return SignItem(word: number.toString(), category: 'Numbers', imagePath: 'assets/numbers/$number.png');
  }),
];