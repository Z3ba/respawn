# Respawn

Mobilna prodavnica gaming opreme - Kontrolna tačka 1, Mobilne informacione tehnologije.

**Autor:** David Zejbeki, IT27/2024.

**GitHub:** https://github.com/Z3ba/respawn (javni repozitorijum).

Android debug APK je uspešno izgrađen i potpis proveren. Lokalna kopija je u `output/android/respawn-kt1-debug.apk`; njeni metapodaci su u `docs/apk-metadata.json`. Pokretanje na telefonu/emulatoru još nije potvrđeno: virtualizacija je isključena u firmware-u računara, a softverski emulator nije postao dostupan.

## Trenutno stanje

KT1 sadrži početnu Flutter aplikaciju sa četiri sekcije, praznim stanjima i pamćenjem teme, Express servis sa `/health`, domenske modele, dokumentaciju i lokalni UI/UX prototip. Firebase, stvarni katalog, nalozi, administracija i checkout još nisu implementirani. Stripe je planiran u test režimu uz plaćanje pouzećem.

Prototip prikazuje **planirani izgled i izmišljene primere proizvoda**; ti podaci nisu ugrađeni u mobilnu aplikaciju. GitHub repozitorijum je javan. Za KT1 je izabran lokalni prototip; Figma je odložena za kasniju fazu. Status predaje: [docs/submission-checklist.md](docs/submission-checklist.md).

## Organizacija

```text
mobile/                 Flutter aplikacija, Android i web pregled
  lib/core/             Tema i zajednička konfiguracija
  lib/models/           Korisnik, kategorija, proizvod, korpa, porudžbina
  lib/providers/        Stanje kataloga i teme
  lib/repositories/     Granica između podataka i prikaza
  lib/screens/          Početna, pretraga, korpa, profil
  lib/services/         HTTP klijent za backend
  lib/widgets/          Zajedničke UI komponente
backend/                Express servis i testovi
docs/                   Tehnički dokument, koncept i provere
docs/design/            Lokalni interaktivni prototip i SVG ekrani
docs/tools/             Ponovljiva izrada prototipa i PDF-a
output/kt1/             Dokument za pregled/predaju
```

## Mobilna aplikacija

Preduslovi: Flutter stable (provereno 3.47.9 / Dart 3.13.7), pun JDK 21, Android SDK i emulator ili povezan Android telefon. Flutter SDK nije deo Git repozitorijuma. Ako postoji lokalna instalacija u `.tools/flutter`, koristi `.\scripts\flutter.ps1` iz korena projekta; ona ne menja globalni PATH i čuva paketni keš lokalno.

```powershell
cd mobile
flutter pub get
flutter analyze
flutter test
flutter devices
flutter run -d <ANDROID_DEVICE_ID>
flutter build apk --debug
```

Na ovom računaru Android SDK, pun Temurin JDK 21 i Gradle keš nalaze se u `D:\RespawnTools`. Za novu terminalsku sesiju iz korena projekta:

```powershell
.\scripts\use-android.ps1 -UseWindowsTrustStore
.\scripts\flutter.ps1 analyze --no-pub
.\scripts\flutter.ps1 test --no-pub
.\scripts\flutter.ps1 build apk --debug --no-pub
```

`-UseWindowsTrustStore` koristi postojeće pouzdane Windows sertifikate u trenutnom procesu; TLS provera ostaje uključena. Lokalni `mobile/build` je junction ka `D:\RespawnTools\build\mobile`, zbog malog slobodnog prostora na C:. SDK i build izlazi se ne šalju na GitHub.

Za pregled na računaru: `flutter run -d chrome`. Web pregled nije zamena za proveru Android aplikacije. Trenutni HTTP klijent je pripremljen, ali UI još ne poziva backend.

Za instalaciju Android alata pripremljena je `scripts/setup-android.ps1`. Ona zahteva putanju do JDK-a i izričito prihvatanje Android SDK licence preko `-AcceptSdkLicense`; `-IncludeEmulator` dodaje emulator i AOSP sistemsku sliku. Podrazumevani direktorijum je `D:\RespawnTools`. Korisnik je potvrdio SDK licencu; status instalacije i Android provere nalazi se u docs/validation.md.

## Backend

Preduslov: Node.js 22+.

```powershell
cd backend
Copy-Item .env.example .env
npm ci
npm test
npm start
```

Provera: `Invoke-RestMethod http://127.0.0.1:3000/health`.

Odgovor: `{"status":"ok","service":"respawn-api","version":"0.1.0"}`. Backend podrazumevano sluša samo na `127.0.0.1`. Za Android emulator u budućoj integraciji koristi `10.0.2.2`; za telefon je potrebna dostupna adresa računara. HTTP je namenjen lokalnom razvoju, a budući deployment koristi HTTPS.

## Dokumentacija i prototip

- Izvor teksta: `docs/KT1-IT27-2024.md`.
- PDF: `output/kt1/KT1-IT27-2024.pdf`.
- Prototip: otvori `docs/design/index.html` u pregledaču. Ne traži server niti pristup internetu.
- SVG ekrani: `docs/design/screens/`. Mogu se uvesti u Figmu kao početni uređivi vizuelni materijal; lokalni HTML linkovi se ne pretvaraju automatski u Figma interakcije.
- Rezultati provera: `docs/validation.md`.

Ponovna izrada: Python sa paketima `reportlab` i `Pillow`, zatim `python docs/tools/build_prototype.py` i `python docs/tools/build_document.py`. Podaci o autoru i linkovima su u `docs/project-metadata.json`. Posle unosa stvarnih GitHub/Figma linkova ponovo izgenerisati PDF.

## Plan naredne faze

Firebase Authentication i Firestore; serverska autorizacija i administracija; CRUD proizvoda, korisnički profil, korpa i omiljeno; checkout pouzećem; Stripe PaymentSheet i verifikovani webhook. Podatke o cenama server čita iz baze, a kartični podaci se ne čuvaju u našoj aplikaciji.

Tajne se čuvaju van repozitorijuma. Primer konfiguracije ne sadrži stvarne ključeve. Korisnička uloga dolazi iz pouzdanog serverskog izvora; lokalni izbor ekrana nije autorizacija.

## Dokumentacija KT1 - dopuna 12.11.2026.

Dokument prati dogovoreni obim: namena i koncept, tehnologije, inicijalni projekat, početni UI/UX koncept i izvori. Sadržaj se automatski izračunava. Aktuelni PDF je `output/kt1/KT1-IT27-2024.pdf`; ranije varijante u output/pdf su lokalne prethodne kopije. Prezentacija MIT_Vezbe2.pptx.pdf uzeta je kao izvor za Flutter razvojno okruženje, bez proglašavanja primera paketa obaveznim projektnim zahtevima.

Prikazi Početne i Profila u dokumentu renderovani su iz stvarnog Flutter koda; nisu Android screenshot-ovi. Za osvežavanje prikaza, posle web build-a iz korena projekta pokrenuti `scripts/flutter.ps1 test --no-pub ../docs/tools/capture_initial_app_test.dart`. Potom pokrenuti `python docs/tools/build_document.py`.
