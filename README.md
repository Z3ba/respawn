# Respawn

Mobilna prodavnica gaming opreme - Kontrolna tačka 1, Mobilne informacione tehnologije.

**Autor:** David Zejbeki, IT27/2024.

**GitHub:** https://github.com/Z3ba/respawn (privatni repozitorijum; pristup predmetnom asistentu dodeliti pre predaje).

## Trenutno stanje

KT1 sadrži početnu Flutter aplikaciju sa četiri sekcije, praznim stanjima i pamćenjem teme, Express servis sa `/health`, domenske modele, dokumentaciju i lokalni UI/UX prototip. Firebase, stvarni katalog, nalozi, administracija i checkout još nisu implementirani. Stripe je planiran u test režimu uz plaćanje pouzećem.

Prototip prikazuje **planirani izgled i izmišljene primere proizvoda**; ti podaci nisu ugrađeni u mobilnu aplikaciju. GitHub repozitorijum je napravljen. Figma URL još nije dostupan jer pristup nalogu nije uspostavljen. Status predaje: [docs/submission-checklist.md](docs/submission-checklist.md).

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
output/pdf/             Dokument za pregled/predaju
```

## Mobilna aplikacija

Preduslovi: Flutter stable, Android Studio/Android SDK i emulator ili povezan Android telefon. Flutter SDK nije deo Git repozitorijuma. Ako postoji lokalna instalacija u `.tools/flutter`, koristi `.\scripts\flutter.ps1` iz korena projekta; ona ne menja globalni PATH i čuva paketni keš lokalno.

```powershell
cd mobile
flutter pub get
flutter analyze
flutter test
flutter devices
flutter run -d <ANDROID_DEVICE_ID>
flutter build apk --debug
```

Za pregled na računaru: `flutter run -d chrome`. Web pregled nije zamena za proveru Android aplikacije. Trenutni HTTP klijent je pripremljen, ali UI još ne poziva backend.

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
- PDF: `output/pdf/KT1-IT27-2024.pdf`.
- Prototip: otvori `docs/design/index.html` u pregledaču. Ne traži server niti pristup internetu.
- SVG ekrani: `docs/design/screens/`. Mogu se uvesti u Figmu kao početni uređivi vizuelni materijal; lokalni HTML linkovi se ne pretvaraju automatski u Figma interakcije.
- Rezultati provera: `docs/validation.md`.

Ponovna izrada: Python sa paketima `reportlab` i `Pillow`, zatim `python docs/tools/build_prototype.py` i `python docs/tools/build_document.py`. Podaci o autoru i linkovima su u `docs/project-metadata.json`. Posle unosa stvarnih GitHub/Figma linkova ponovo izgenerisati PDF.

## Plan naredne faze

Firebase Authentication i Firestore; serverska autorizacija i administracija; CRUD proizvoda, korisnički profil, korpa i omiljeno; checkout pouzećem; Stripe PaymentSheet i verifikovani webhook. Podatke o cenama server čita iz baze, a kartični podaci se ne čuvaju u našoj aplikaciji.

Tajne se čuvaju van repozitorijuma. Primer konfiguracije ne sadrži stvarne ključeve. Korisnička uloga dolazi iz pouzdanog serverskog izvora; lokalni izbor ekrana nije autorizacija.
