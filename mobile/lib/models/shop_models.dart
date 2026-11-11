enum UserRole { customer, admin }

enum PaymentMethod { cashOnDelivery, stripeTest }

enum OrderStatus {
  pendingPayment,
  placed,
  processing,
  shipped,
  completed,
  cancelled,
}

class AppUser {
  const AppUser({
    required this.id,
    required this.displayName,
    required this.email,
    this.role = UserRole.customer,
  });
  final String id;
  final String displayName;
  final String email;
  final UserRole role;
}

class Category {
  const Category({required this.id, required this.name});
  final String id;
  final String name;
}

class Product {
  const Product({
    required this.id,
    required this.categoryId,
    required this.name,
    required this.description,
    required this.priceMinor,
    required this.stock,
    this.imageUrl,
    this.attributes = const {},
  });
  final String id;
  final String categoryId;
  final String name;
  final String description;
  // Integer minor currency units. Formatting belongs in the presentation layer.
  final int priceMinor;
  final int stock;
  final String? imageUrl;
  final Map<String, String> attributes;
}

class CartItem {
  const CartItem({required this.productId, required this.quantity});
  final String productId;
  final int quantity;
}

class OrderItem {
  const OrderItem({
    required this.productId,
    required this.productName,
    required this.quantity,
    required this.unitPriceMinor,
  });
  final String productId;
  final String productName;
  final int quantity;
  final int unitPriceMinor;
}

class DeliveryAddress {
  const DeliveryAddress({
    required this.fullName,
    required this.phone,
    required this.street,
    required this.city,
    required this.postalCode,
  });
  final String fullName;
  final String phone;
  final String street;
  final String city;
  final String postalCode;
}

class ShopOrder {
  const ShopOrder({
    required this.id,
    required this.userId,
    required this.items,
    required this.deliveryAddress,
    required this.totalMinor,
    required this.currency,
    required this.paymentMethod,
    required this.status,
    required this.createdAt,
  });
  final String id;
  final String userId;
  final List<OrderItem> items;
  final DeliveryAddress deliveryAddress;
  final int totalMinor;
  final String currency;
  final PaymentMethod paymentMethod;
  final OrderStatus status;
  final DateTime createdAt;
}
