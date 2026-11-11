import 'package:flutter/foundation.dart';
import '../models/shop_models.dart';
import '../repositories/catalog_repository.dart';

class CatalogProvider extends ChangeNotifier {
  CatalogProvider(this._repository);
  final CatalogRepository _repository;
  List<Product> _products = const [];
  bool _loading = true;
  bool _hasError = false;
  bool _disposed = false;
  List<Product> get products => List.unmodifiable(_products);
  bool get loading => _loading;
  bool get hasError => _hasError;

  Future<void> load() async {
    _loading = true;
    _hasError = false;
    notifyListeners();
    try {
      _products = await _repository.fetchProducts();
    } catch (_) {
      _hasError = true;
    }
    _loading = false;
    if (!_disposed) notifyListeners();
  }

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }
}
