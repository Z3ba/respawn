# Evidencija provera - KT1

Datum: 11.11.2026. Autor: David Zejbeki, IT27/2024.

## Okruženje

- Windows 10, Node.js 24.14.1, npm 11.11.0.
- Flutter stable 3.47.9 i Dart 3.13.7; SDK i paketni keš su lokalni i izostavljeni iz Git-a.
- Pun Eclipse Temurin JDK 21.0.13+9 instaliran u D:\RespawnTools\jdk21. Postojeća Eclipse Java 21 nema jlink i ne koristi se za Android build.
- Android SDK u D:\RespawnTools\android-sdk: platforme 35/36, Build Tools 36.0.0, NDK 28.2.13676358, CMake 3.22.1, platform-tools, emulator i AOSP API 35 x86_64 slika. Korisnik je izričito prihvatio SDK licencu i ovu instalaciju.
- Flutter i JDK arhive proverene su SHA256 vrednostima zvaničnih izvora. SDK i JDK nisu deo repozitorijuma.
- Gradle keš je na D:. Generisani mobile/build je junction ka D:\RespawnTools\build\mobile; izvorni kod i dokumentacija ostaju u projektnom folderu na C:.
- Java mrežni pozivi koriste postojeće Windows-ROOT sertifikate samo u procesu. TLS verifikacija nije isključena i sistemska skladišta sertifikata nisu menjana.

## Automatizovane provere

| Provera | Rezultat |
| --- | --- |
| flutter pub get | Uspešno; razrešene verzije su u mobile/pubspec.lock |
| flutter analyze --no-pub | No issues found |
| flutter test --no-pub | 2 testa prolaze |
| npm test u backend direktorijumu | 3 testa prolaze |
| npm start i HTTP GET /health | HTTP 200; status ok, respawn-api, 0.1.0 |
| flutter build web --no-pub --base-href=/mobile/build/web/ --no-web-resources-cdn | Uspešan build |
| flutter build apk --debug --no-pub | Uspešan Android build, izlazni kod 0 |
| apksigner verify --verbose | Potpis ispravan, APK Signature Scheme v2 |
| aapt dump badging | Respawn, rs.respawn.respawn, 0.1.0, minSdk 24, targetSdk 36 |
| ZIP CRC i struktura APK-a | Ispravno; manifest, classes.dex i tri Flutter ABI biblioteke |

Widget testovi proveravaju gostujuću navigaciju, unos pretrage, praznu korpu i povratak na istraživanje, profil i pamćenje teme nakon ponovnog kreiranja aplikacije. Backend testovi koriste stvarni lokalni HTTP listener i proveravaju /health, 404 za neimplementirani checkout i odbijanje neispravnog PORT podešavanja.

APK je lokalno pripremljen u output/android/respawn-kt1-debug.apk. Veličina i SHA256 su u docs/apk-metadata.json. Binarni APK i build keš se ne šalju u Git; izvorni kod i uputstvo za build jesu objavljeni.

## Vizuelne provere

- Flutter web aplikacija pregledana je na desktop i mobilnoj širini 390 px, uključujući početni ekran i profil. Nema uočenog preklapanja sadržaja ili navigacije.
- Lokalni prototip sadrži 14 ekrana; provereno je da nema linkova ka nepostojećim ekranima.
- U pregledaču je prođen tok katalog -> detalji -> korpa -> dostava -> plaćanje -> neuspeh -> ponovni pokušaj -> uspeh -> porudžbine.
- SVG ekrani sadrže uređive oblike i tekst. Primeri proizvoda postoje samo u dizajnu, ne u aplikacionom katalogu.
- PDF je renderovan Poppler-om i vizuelno pregledan: naslovna strana, tabele, prikazi prototipa i završni klikabilni GitHub link.

## Granice provere

Android APK je izgrađen i potpis proveren, ali pokretanje na Android uređaju nije potvrđeno. Napravljen je zaseban Respawn_KT1_API35 emulator. Emulator hypervisor nije instaliran, a Win32_Processor prijavljuje VirtualizationFirmwareEnabled=False. Dva pokušaja softverskog rada nisu dovela do online uređaja; test emulator je potom ugašen. BIOS, Windows bezbednosne opcije i drajveri nisu menjani. Završiti ovu proveru na fizičkom telefonu ili nakon ručnog podešavanja virtualizacije i emulatora.

Figma je izričitim izborom korisnika odložena. Lokalni HTML prototip i SVG ekrani predstavljaju dogovoreni dizajnerski rezultat KT1.

## GitHub

Javni repozitorijum: https://github.com/Z3ba/respawn. Grana codex/kt1-respawn je podrazumevana. Objavljeni su kod, testovi, dokumentacija, lokalni prototip i PDF. SDK, node_modules, build izlazi, APK i .env fajlovi izostavljeni su iz Git istorije.

## Ponovna provera

Iz korena projekta: scripts/use-android.ps1 -UseWindowsTrustStore, zatim scripts/flutter.ps1 analyze --no-pub, scripts/flutter.ps1 test --no-pub i scripts/flutter.ps1 build apk --debug --no-pub. U backend direktorijumu: npm ci, npm test i npm start. PDF/SVG zavisnosti su navedene u docs/tools/requirements.txt.

## Dopuna dokumentacije 12.11.2026.

PDF je reorganizovan po dogovorenom KT1 planu i prikazan u akademskom stilu po KT3 primeru, uz sadržaj sa automatskim brojevima stranica. Dodati su prikaz strukture i dva rendera početne aplikacije. Izvoz rendera je uspešno izvršen Flutter test renderer-om, sa Roboto i MaterialIcons fontovima. Prezentacija MIT_Vezbe2.pptx.pdf pregledana je tekstualno i vizuelno; beleška o alatima i statusu primera paketa uključena je u poglavlje 2. Završni dokument ima 10 PDF stranica, odnosno naslovnu, sadržaj i osam numerisanih stranica. Svi listovi renderovani su i vizuelno pregledani. Aktuelni izlaz: output/kt1/KT1-IT27-2024.pdf.

### Ispravka strukture prema KT3 primeru

Nazivi i redosled glavnih poglavlja usklađeni su sa KT3 primerom (1-5). Definicije i uloge su u poglavlju 3, struktura i modeli u poglavlju 4, a prikazi ekrana u poglavlju 5. Izvori su zaseban završni dodatak. PDF ima 13 strana: naslovna, sadržaj i 11 numerisanih stranica. Provereni su prelom, automatski sadržaj, prikazi i završni link.
