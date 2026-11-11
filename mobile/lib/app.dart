import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'core/theme.dart';
import 'providers/catalog_provider.dart';
import 'providers/theme_provider.dart';
import 'repositories/catalog_repository.dart';
import 'screens/root_screen.dart';

class RespawnApp extends StatelessWidget {
  const RespawnApp({super.key, required this.preferences});
  final SharedPreferences preferences;

  @override
  Widget build(BuildContext context) => MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (_) => ThemeProvider(preferences)),
      ChangeNotifierProvider(
        create: (_) =>
            CatalogProvider(const PendingCatalogRepository())..load(),
      ),
    ],
    child: Consumer<ThemeProvider>(
      builder: (context, theme, child) => MaterialApp(
        title: 'Respawn',
        debugShowCheckedModeBanner: false,
        theme: RespawnTheme.light,
        darkTheme: RespawnTheme.dark,
        themeMode: theme.mode,
        locale: const Locale('sr'),
        supportedLocales: const [Locale('sr'), Locale('en')],
        localizationsDelegates: GlobalMaterialLocalizations.delegates,
        home: const RootScreen(),
      ),
    ),
  );
}
