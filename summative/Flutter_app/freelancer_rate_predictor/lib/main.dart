import 'package:flutter/material.dart';

import 'screens/prediction_screen.dart';

void main() {
  runApp(const FreelancerRateApp());
}

class FreelancerRateApp extends StatelessWidget {
  const FreelancerRateApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Freelancer Rate Predictor',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorSchemeSeed: Colors.teal,
        useMaterial3: true,
      ),
      home: const PredictionScreen(),
    );
  }
}
