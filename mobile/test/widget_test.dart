import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:respawn/app.dart';

void main() {
  Future<void> launch(WidgetTester tester) async {
    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();
    await tester.pumpWidget(RespawnApp(preferences: prefs));
    await tester.pumpAndSettle();
  }

  testWidgets('guest can navigate all tabs and return from an empty cart', (
    tester,
  ) async {
    await launch(tester);
    expect(find.text('Tvoj sledeći\nupgrade.'), findsOneWidget);
    await tester.tap(find.text('Pretraga').last);
    await tester.pumpAndSettle();
    await tester.enterText(find.byType(TextField), 'tastatura');
    await tester.pumpAndSettle();
    expect(find.text('Nema pronađenih proizvoda'), findsOneWidget);
    await tester.tap(find.text('Korpa').last);
    await tester.pumpAndSettle();
    expect(find.text('Korpa je prazna'), findsOneWidget);
    await tester.tap(find.widgetWithText(FilledButton, 'Istraži ponudu').last);
    await tester.pumpAndSettle();
    expect(find.text('Šta tražiš za svoj setup?'), findsOneWidget);
    await tester.tap(find.text('Profil').last);
    await tester.pumpAndSettle();
    expect(find.text('Tvoja oprema. Tvoj nalog.'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('theme choice survives application recreation', (tester) async {
    await launch(tester);
    await tester.tap(find.text('Profil').last);
    await tester.pumpAndSettle();
    await tester.tap(find.byType(Switch));
    await tester.pumpAndSettle();
    expect((await SharedPreferences.getInstance()).getBool('darkTheme'), false);
    await tester.pumpWidget(const SizedBox.shrink());
    await tester.pumpWidget(
      RespawnApp(preferences: await SharedPreferences.getInstance()),
    );
    await tester.pumpAndSettle();
    final context = tester.element(find.byType(Scaffold));
    expect(Theme.of(context).brightness, Brightness.light);
    expect(tester.takeException(), isNull);
  });
}
