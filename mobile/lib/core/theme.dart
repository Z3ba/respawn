import 'package:flutter/material.dart';

abstract final class RespawnTheme {
  static const accent = Color(0xFFBDA4FF);
  static const background = Color(0xFF111116);
  static const surface = Color(0xFF1D1D25);

  static ThemeData get dark => _theme(Brightness.dark);
  static ThemeData get light => _theme(Brightness.light);

  static ThemeData _theme(Brightness brightness) {
    final dark = brightness == Brightness.dark;
    final scheme =
        ColorScheme.fromSeed(
          seedColor: const Color(0xFF8055DC),
          brightness: brightness,
        ).copyWith(
          primary: dark ? accent : const Color(0xFF6541AE),
          surface: dark ? surface : const Color(0xFFF4F1FA),
        );
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: dark ? background : const Color(0xFFFCFAFF),
      appBarTheme: AppBarTheme(
        backgroundColor: dark ? background : const Color(0xFFFCFAFF),
        elevation: 0,
        centerTitle: false,
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: BorderSide.none,
        ),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: dark ? surface : const Color(0xFFF4F1FA),
        indicatorColor: dark
            ? const Color(0xFF3C2D59)
            : const Color(0xFFE7DAFF),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          minimumSize: const Size(48, 48),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
      ),
    );
  }
}
