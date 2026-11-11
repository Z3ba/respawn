import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ThemeProvider extends ChangeNotifier {
  ThemeProvider(this._preferences)
    : _dark = _preferences.getBool('darkTheme') ?? true;
  final SharedPreferences _preferences;
  bool _dark;
  bool get isDark => _dark;
  ThemeMode get mode => _dark ? ThemeMode.dark : ThemeMode.light;

  Future<void> setDark(bool value) async {
    _dark = value;
    notifyListeners();
    await _preferences.setBool('darkTheme', value);
  }
}
