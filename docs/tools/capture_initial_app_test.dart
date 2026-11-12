import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:respawn/app.dart';
void main() {
 testWidgets('Render initial application for project documentation', (tester) async {
  tester.view.physicalSize = const Size(390,844);
  tester.view.devicePixelRatio = 1;
  await tester.runAsync(() async {
  final loader=FontLoader('Roboto');
  final data=await File('../.tools/flutter/engine/src/flutter/txt/third_party/fonts/Roboto-Regular.ttf').readAsBytes();
  loader.addFont(Future.value(ByteData.sublistView(data)));await loader.load();
  final icons=FontLoader('MaterialIcons');
  final iconBytes=await File('build/web/assets/fonts/MaterialIcons-Regular.otf').readAsBytes();
  icons.addFont(Future.value(ByteData.sublistView(iconBytes)));await icons.load();
  });
  SharedPreferences.setMockInitialValues({});
  final prefs=await SharedPreferences.getInstance();final key=GlobalKey();
  await tester.pumpWidget(RepaintBoundary(key:key,child:RespawnApp(preferences:prefs)));
  await tester.pumpAndSettle();
  Future<void> save(String name) async {
   final boundary=key.currentContext!.findRenderObject()! as RenderRepaintBoundary;
   final im=await boundary.toImage(pixelRatio:2);
   final bytes=await im.toByteData(format:ui.ImageByteFormat.png);
   await File('../docs/images/$name.png').writeAsBytes(bytes!.buffer.asUint8List());im.dispose();
  }
  await tester.runAsync(()=>save('initial-home'));
  await tester.tap(find.text('Profil').last);await tester.pumpAndSettle();
  await tester.runAsync(()=>save('initial-profile'));
 });
}
