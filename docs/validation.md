# Evidencija provera - KT1

Datum: 11.11.2026. Autor: David Zejbeki, IT27/2024.

## Razvojno okruženje

- Windows 10; Node.js 24.14.1; npm 11.11.0.
- Lokalno pripremljen Flutter stable 3.47.9, Dart 3.13.7. SDK i paketni keš nisu deo repozitorijuma.
- Arhiva SDK-a pre raspakivanja proverena je SHA256 vrednošću iz zvaničnog manifesta. Zbog prostora izostavljeni su nepotrebni engine simboli i desktop build artefakti; alati potrebni za izvršene provere su dostupni.
- Flutter native hooks na Windowsu prijavili su problem sa razmacima u SDK putanji. Za provere i skriptu koristi se postojeća Windows 8.3 kratka putanja, bez preimenovanja projekta.
- Android SDK nije pronađen. Dostupna Java iz PATH-a je 1.8.0_51; Android projekat zahteva savremen JDK. Nijedan Android uređaj ili emulator nije dostupan.

## Automatizovane provere

| Provera | Rezultat |
| --- | --- |
| `flutter pub get` | Uspešno; verzije su u mobile/pubspec.lock |
| `flutter analyze --no-pub` | No issues found |
| `flutter test --no-pub` | 2 testa prolaze |
| `npm test` u backend direktorijumu | 3 testa prolaze |
| `flutter build web --no-pub --base-href=/mobile/build/web/ --no-web-resources-cdn` | Uspešno izgrađen build/web |
| `flutter build apk --debug --no-pub` | APK nije kreiran: No Android SDK found |

Widget testovi proveravaju gostujuću navigaciju, unos pretrage, praznu korpu i povratak u pretragu, profil i trajno pamćenje svetle teme posle ponovnog kreiranja aplikacije. Backend testovi koriste stvarni lokalni HTTP listener: zdravstvena provera, 404 za neimplementirani checkout i odbijanje neispravnog PORT podešavanja.

Web build je prijavio informativno upozorenje o nedostajućem Cupertino fontu; aplikacija koristi Material ikone i build je uspešan. Web build nije zamena za Android build ili test na telefonu.

## Vizuelne i ručne provere

- Flutter web aplikacija otvorena je u pregledaču. Pregledane su desktop i mobilna širina 390 px, početni ekran i profil. Glavni sadržaj i navigacija ostaju u okviru prikaza.
- Lokalni UI/UX prototip sadrži 14 ekrana i nema linkova ka nepostojećim ekranima.
- U pregledaču je prođen tok: katalog -> detalji -> korpa -> dostava -> plaćanje -> neuspeh -> ponovni pokušaj -> uspeh -> porudžbine.
- SVG elementi su semantičke forme i tekst; nisu screenshot cele aplikacije. Primeri proizvoda postoje samo u dizajnu.
- PDF je izgrađen iz Markdown izvora, renderovan Poppler-om i vizuelno pregledan. Završni PDF ima 10 strana; proverene su naslovna strana, tabele, prikazi prototipa i završni GitHub link.

## Otvorene stavke

1. Instalirati Android Studio/SDK i odgovarajući JDK, prihvatiti potrebne uslove i pokrenuti aplikaciju na emulatoru ili telefonu. Instalacija emulatora i sistemske slike nije završena zbog nedostajućeg okruženja i ograničenog slobodnog prostora.
2. Figma alat i alat za povezivanje dodataka u ovoj sesiji vraćaju da nisu dostupni. Pregledač prikazuje ekran za prijavu. Lokalni HTML/SVG materijali su pripremljeni, ali Figma fajl i Figma prototipske interakcije nisu objavljeni niti verifikovani.
3. Status GitHub objave i stvarni URL vode se u docs/project-metadata.json. Ako je repozitorijum privatan, pristup predmetnom asistentu mora biti posebno omogućen pre predaje.

## Ponovna provera

Iz korena projekta koristiti `scripts/flutter.ps1 analyze --no-pub` i `scripts/flutter.ps1 test --no-pub`, ili standardni Flutter SDK bez razmaka u putanji. U backend direktorijumu pokrenuti `npm ci` i `npm test`. Za PDF i SVG pripremiti zavisnosti iz docs/tools/requirements.txt.
