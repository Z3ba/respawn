import 'dart:convert';
import 'package:http/http.dart' as http;

class BackendService {
  BackendService({required this.baseUrl, required this.client});
  // Local Android emulator uses http://10.0.2.2:3000.
  // Pass an HTTPS base URL for future deployed environments.
  final Uri baseUrl;
  final http.Client client;

  Future<bool> isHealthy() async {
    final response = await client
        .get(baseUrl.resolve('/health'))
        .timeout(const Duration(seconds: 10));
    if (response.statusCode != 200) return false;
    final data = jsonDecode(response.body);
    return data is Map<String, dynamic> && data['status'] == 'ok';
  }
}
