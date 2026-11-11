import '../models/shop_models.dart';

abstract interface class CatalogRepository {
  Future<List<Product>> fetchProducts();
}

// KT1 boundary: no sample catalog is embedded in the application.
// Replace this adapter with FirestoreCatalogRepository in the next phase.
class PendingCatalogRepository implements CatalogRepository {
  const PendingCatalogRepository();
  @override
  Future<List<Product>> fetchProducts() async => const [];
}
