import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/catalog_provider.dart';
import '../providers/theme_provider.dart';
import '../widgets/empty_state.dart';

class RootScreen extends StatefulWidget {
  const RootScreen({super.key});
  @override
  State<RootScreen> createState() => _RootScreenState();
}

class _RootScreenState extends State<RootScreen> {
  int _index = 0;
  final _search = TextEditingController();
  void _browse([String category = '']) {
    _search.text = category;
    setState(() => _index = 1);
  }

  @override
  void dispose() {
    _search.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: const Text(
        'respawn.',
        style: TextStyle(
          fontWeight: FontWeight.w900,
          letterSpacing: -1,
          fontSize: 29,
        ),
      ),
      actions: [
        IconButton(
          tooltip: 'Profil',
          onPressed: () => setState(() => _index = 3),
          icon: const Icon(Icons.person_outline_rounded),
        ),
        const SizedBox(width: 8),
      ],
    ),
    body: SafeArea(
      child: LayoutBuilder(
        builder: (context, constraints) => Center(
          child: SizedBox(
            width: constraints.maxWidth > 680 ? 680 : constraints.maxWidth,
            child: IndexedStack(
              index: _index,
              children: [
                _home(context),
                _searchPage(context),
                _cart(context),
                _profile(context),
              ],
            ),
          ),
        ),
      ),
    ),
    bottomNavigationBar: NavigationBar(
      selectedIndex: _index,
      onDestinationSelected: (value) => setState(() => _index = value),
      destinations: const [
        NavigationDestination(
          icon: Icon(Icons.home_outlined),
          selectedIcon: Icon(Icons.home_rounded),
          label: 'Početna',
        ),
        NavigationDestination(
          icon: Icon(Icons.search_rounded),
          label: 'Pretraga',
        ),
        NavigationDestination(
          icon: Icon(Icons.shopping_bag_outlined),
          selectedIcon: Icon(Icons.shopping_bag_rounded),
          label: 'Korpa',
        ),
        NavigationDestination(
          icon: Icon(Icons.person_outline_rounded),
          selectedIcon: Icon(Icons.person_rounded),
          label: 'Profil',
        ),
      ],
    ),
  );

  Widget _home(BuildContext context) => ListView(
    key: const PageStorageKey('home'),
    padding: const EdgeInsets.all(24),
    children: [
      Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF4B2B7F), Color(0xFF272036)],
          ),
          borderRadius: BorderRadius.circular(24),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'LEVEL UP YOUR SETUP',
              style: TextStyle(
                color: Color(0xFFD6C5FF),
                fontSize: 11,
                letterSpacing: 2,
                fontWeight: FontWeight.w700,
              ),
            ),
            const SizedBox(height: 18),
            const Text(
              'Tvoj sledeći\nupgrade.',
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.w800,
                fontSize: 36,
                height: 1.1,
              ),
            ),
            const SizedBox(height: 12),
            const Text(
              'Gaming oprema za tvoj način igre.',
              style: TextStyle(color: Color(0xFFDED5F0), height: 1.5),
            ),
            const SizedBox(height: 22),
            FilledButton.icon(
              onPressed: _browse,
              icon: const Icon(Icons.arrow_forward_rounded),
              label: const Text('Istraži ponudu'),
            ),
          ],
        ),
      ),
      const SizedBox(height: 28),
      Text(
        'Pronađi svoju opremu',
        style: Theme.of(
          context,
        ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
      ),
      const SizedBox(height: 14),
      Wrap(
        spacing: 8,
        runSpacing: 8,
        children: [
          for (final category in [
            'Tastature',
            'Miševi',
            'Slušalice',
            'Podloge',
          ])
            ActionChip(
              label: Text(category),
              onPressed: () => _browse(category),
            ),
        ],
      ),
      const SizedBox(height: 8),
      Consumer<CatalogProvider>(
        builder: (context, catalog, child) {
          if (catalog.loading) {
            return const Padding(
              padding: EdgeInsets.all(40),
              child: Center(child: CircularProgressIndicator()),
            );
          }
          if (catalog.hasError) {
            return EmptyState(
              icon: Icons.wifi_off_rounded,
              title: 'Ponuda trenutno nije dostupna',
              message: 'Pokušaj ponovo za nekoliko trenutaka.',
              actionLabel: 'Pokušaj ponovo',
              onAction: catalog.load,
            );
          }
          return const EmptyState(
            icon: Icons.sports_esports_outlined,
            title: 'Ponuda uskoro stiže',
            message: 'Ovde ćeš pronaći opremu za svoj sledeći nivo igre.',
          );
        },
      ),
    ],
  );

  Widget _searchPage(BuildContext context) => ListView(
    padding: const EdgeInsets.all(24),
    children: [
      _heading(context, 'Pretraga'),
      const SizedBox(height: 20),
      TextField(
        controller: _search,
        onChanged: (_) => setState(() {}),
        decoration: InputDecoration(
          labelText: 'Pretraži opremu',
          hintText: 'Naziv, brend ili kategorija',
          prefixIcon: const Icon(Icons.search),
          suffixIcon: IconButton(
            tooltip: 'Obriši pretragu',
            onPressed: () {
              _search.clear();
              setState(() {});
            },
            icon: const Icon(Icons.close_rounded),
          ),
        ),
      ),
      const SizedBox(height: 24),
      EmptyState(
        icon: Icons.search_rounded,
        title: _search.text.trim().isEmpty
            ? 'Šta tražiš za svoj setup?'
            : 'Nema pronađenih proizvoda',
        message: 'Katalog trenutno nema dostupnih proizvoda.',
      ),
    ],
  );

  Widget _cart(BuildContext context) => ListView(
    padding: const EdgeInsets.all(24),
    children: [
      _heading(context, 'Tvoja korpa'),
      EmptyState(
        icon: Icons.shopping_bag_outlined,
        title: 'Korpa je prazna',
        message: 'Tvoj sledeći upgrade počinje izborom opreme.',
        actionLabel: 'Istraži ponudu',
        onAction: _browse,
      ),
    ],
  );

  Widget _profile(BuildContext context) => ListView(
    padding: const EdgeInsets.all(24),
    children: [
      _heading(context, 'Tvoj profil'),
      const EmptyState(
        icon: Icons.person_outline_rounded,
        title: 'Tvoja oprema. Tvoj nalog.',
        message:
            'Prijava i registracija biće dostupne uskoro. Sa nalogom ćeš moći da sačuvaš omiljenu opremu i pratiš porudžbine.',
      ),
      const Divider(),
      Consumer<ThemeProvider>(
        builder: (context, theme, child) => SwitchListTile(
          contentPadding: EdgeInsets.zero,
          secondary: const Icon(Icons.dark_mode_outlined),
          title: const Text('Tamna tema'),
          value: theme.isDark,
          onChanged: theme.setDark,
        ),
      ),
      const SizedBox(height: 20),
      Text('Respawn · 0.1.0', style: Theme.of(context).textTheme.labelMedium),
    ],
  );

  Widget _heading(BuildContext context, String text) => Text(
    text,
    style: Theme.of(
      context,
    ).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w800),
  );
}
