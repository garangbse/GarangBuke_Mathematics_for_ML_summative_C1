// Central place to configure the backend API's base URL.
//
// CHANGE THIS to your deployed API's base URL (e.g. your Render URL).
// Do NOT use "localhost" here if testing on a real phone/emulator,
// since that would point at the device itself, not your computer.
// (Android emulator wanting your own machine's localhost should use
// http://10.0.2.2:8000 instead.)
class ApiConfig {
  static const String baseUrl = 'https://garangbuke-mathematics-for-ml-summative.onrender.com';

  static const String predictEndpoint = '$baseUrl/predict';

  static const Duration requestTimeout = Duration(seconds: 30);
}
