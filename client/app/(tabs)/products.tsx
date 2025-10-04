import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
  RefreshControl,
  Modal,
} from "react-native";
import { useState, useEffect } from "react";
import { useRouter } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { apiService } from "@/services/api";
import { Product, ProductListParams } from "@/types/product";
import { ApiError } from "@/types/auth";
import { storage } from "@/utils/storage";

export default function ProductList() {
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isAdmin, setIsAdmin] = useState(false);

  // Filter states
  const [searchQuery, setSearchQuery] = useState("");
  const [showFilters, setShowFilters] = useState(false);
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [availableOnly, setAvailableOnly] = useState<boolean | undefined>(undefined);

  useEffect(() => {
    checkUserRole();
    loadProducts();
  }, [page]);

  const checkUserRole = async () => {
    const user = await storage.getUser();
    setIsAdmin(user?.role === "admin");
  };

  const loadProducts = async () => {
    try {
      const params: ProductListParams = {
        page,
        limit: 10,
      };

      if (searchQuery) params.q = searchQuery;
      if (minPrice) params.min_price = parseFloat(minPrice);
      if (maxPrice) params.max_price = parseFloat(maxPrice);
      if (availableOnly !== undefined) params.available = availableOnly;

      const response = await apiService.getProducts(params);
      setProducts(response.data.items);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      const apiError = error as ApiError;
      console.error("Error loading products:", apiError.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    setPage(1);
    loadProducts();
  };

  const handleSearch = () => {
    setPage(1);
    loadProducts();
  };

  const clearFilters = () => {
    setSearchQuery("");
    setMinPrice("");
    setMaxPrice("");
    setAvailableOnly(undefined);
    setPage(1);
    setShowFilters(false);
  };

  const applyFilters = () => {
    setPage(1);
    loadProducts();
    setShowFilters(false);
  };

  const renderProduct = ({ item }: { item: Product }) => (
    <TouchableOpacity
      style={styles.productCard}
      onPress={() => router.push(`/products/${item.id}`)}
    >
      <View style={styles.productInfo}>
        <Text style={styles.productName}>{item.name}</Text>
        <Text style={styles.productDescription} numberOfLines={2}>
          {item.description || "No description"}
        </Text>
        <View style={styles.productFooter}>
          <Text style={styles.productPrice}>${parseFloat(item.price.toString()).toFixed(2)}</Text>
          <View style={[styles.stockBadge, item.stock > 0 ? styles.inStock : styles.outOfStock]}>
            <Text style={styles.stockText}>
              {item.stock > 0 ? `${item.stock} in stock` : "Out of stock"}
            </Text>
          </View>
        </View>
      </View>
      <Ionicons name="chevron-forward" size={24} color="#666666" />
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#000000" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Products</Text>
        {isAdmin && (
          <TouchableOpacity
            style={styles.addButton}
            onPress={() => router.push("/products/create")}
          >
            <Ionicons name="add" size={24} color="#ffffff" />
          </TouchableOpacity>
        )}
      </View>

      <View style={styles.searchContainer}>
        <View style={styles.searchInputContainer}>
          <Ionicons name="search" size={20} color="#666666" />
          <TextInput
            style={styles.searchInput}
            placeholder="Search products..."
            value={searchQuery}
            onChangeText={setSearchQuery}
            onSubmitEditing={handleSearch}
          />
        </View>
        <TouchableOpacity
          style={styles.filterButton}
          onPress={() => setShowFilters(true)}
        >
          <Ionicons name="options" size={24} color="#000000" />
        </TouchableOpacity>
      </View>

      <FlatList
        data={products}
        renderItem={renderProduct}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No products found</Text>
          </View>
        }
      />

      {/* Pagination */}
      {totalPages > 1 && (
        <View style={styles.pagination}>
          <TouchableOpacity
            style={[styles.pageButton, page === 1 && styles.pageButtonDisabled]}
            onPress={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
          >
            <Text style={styles.pageButtonText}>Previous</Text>
          </TouchableOpacity>
          <Text style={styles.pageInfo}>
            Page {page} of {totalPages}
          </Text>
          <TouchableOpacity
            style={[
              styles.pageButton,
              page === totalPages && styles.pageButtonDisabled,
            ]}
            onPress={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
          >
            <Text style={styles.pageButtonText}>Next</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Filter Modal */}
      <Modal
        visible={showFilters}
        animationType="slide"
        transparent={true}
        onRequestClose={() => setShowFilters(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Filters</Text>
              <TouchableOpacity onPress={() => setShowFilters(false)}>
                <Ionicons name="close" size={24} color="#000000" />
              </TouchableOpacity>
            </View>

            <View style={styles.filterSection}>
              <Text style={styles.filterLabel}>Price Range</Text>
              <View style={styles.priceInputs}>
                <TextInput
                  style={styles.priceInput}
                  placeholder="Min"
                  keyboardType="numeric"
                  value={minPrice}
                  onChangeText={setMinPrice}
                />
                <Text style={styles.priceSeparator}>-</Text>
                <TextInput
                  style={styles.priceInput}
                  placeholder="Max"
                  keyboardType="numeric"
                  value={maxPrice}
                  onChangeText={setMaxPrice}
                />
              </View>
            </View>

            <View style={styles.filterSection}>
              <Text style={styles.filterLabel}>Availability</Text>
              <View style={styles.availabilityButtons}>
                <TouchableOpacity
                  style={[
                    styles.availabilityButton,
                    availableOnly === undefined && styles.availabilityButtonActive,
                  ]}
                  onPress={() => setAvailableOnly(undefined)}
                >
                  <Text
                    style={[
                      styles.availabilityButtonText,
                      availableOnly === undefined &&
                        styles.availabilityButtonTextActive,
                    ]}
                  >
                    All
                  </Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[
                    styles.availabilityButton,
                    availableOnly === true && styles.availabilityButtonActive,
                  ]}
                  onPress={() => setAvailableOnly(true)}
                >
                  <Text
                    style={[
                      styles.availabilityButtonText,
                      availableOnly === true &&
                        styles.availabilityButtonTextActive,
                    ]}
                  >
                    In Stock
                  </Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[
                    styles.availabilityButton,
                    availableOnly === false && styles.availabilityButtonActive,
                  ]}
                  onPress={() => setAvailableOnly(false)}
                >
                  <Text
                    style={[
                      styles.availabilityButtonText,
                      availableOnly === false &&
                        styles.availabilityButtonTextActive,
                    ]}
                  >
                    Out of Stock
                  </Text>
                </TouchableOpacity>
              </View>
            </View>

            <View style={styles.modalActions}>
              <TouchableOpacity
                style={styles.clearButton}
                onPress={clearFilters}
              >
                <Text style={styles.clearButtonText}>Clear All</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.applyButton}
                onPress={applyFilters}
              >
                <Text style={styles.applyButtonText}>Apply Filters</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f5f5",
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#ffffff",
    padding: 16,
    paddingTop: 50,
    borderBottomWidth: 1,
    borderBottomColor: "#e0e0e0",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#000000",
  },
  addButton: {
    backgroundColor: "#000000",
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: "center",
    alignItems: "center",
  },
  searchContainer: {
    flexDirection: "row",
    padding: 16,
    gap: 12,
    backgroundColor: "#ffffff",
  },
  searchInputContainer: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#f5f5f5",
    borderRadius: 8,
    paddingHorizontal: 12,
    gap: 8,
  },
  searchInput: {
    flex: 1,
    paddingVertical: 12,
    fontSize: 16,
  },
  filterButton: {
    backgroundColor: "#f5f5f5",
    width: 48,
    height: 48,
    borderRadius: 8,
    justifyContent: "center",
    alignItems: "center",
  },
  listContent: {
    padding: 16,
  },
  productCard: {
    flexDirection: "row",
    backgroundColor: "#ffffff",
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  productInfo: {
    flex: 1,
    gap: 4,
  },
  productName: {
    fontSize: 18,
    fontWeight: "600",
    color: "#000000",
  },
  productDescription: {
    fontSize: 14,
    color: "#666666",
  },
  productFooter: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 8,
  },
  productPrice: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#000000",
  },
  stockBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  inStock: {
    backgroundColor: "#e8f5e9",
  },
  outOfStock: {
    backgroundColor: "#ffebee",
  },
  stockText: {
    fontSize: 12,
    fontWeight: "600",
  },
  emptyContainer: {
    padding: 32,
    alignItems: "center",
  },
  emptyText: {
    fontSize: 16,
    color: "#666666",
  },
  pagination: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    backgroundColor: "#ffffff",
    borderTopWidth: 1,
    borderTopColor: "#e0e0e0",
  },
  pageButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: "#000000",
    borderRadius: 8,
  },
  pageButtonDisabled: {
    backgroundColor: "#cccccc",
  },
  pageButtonText: {
    color: "#ffffff",
    fontWeight: "600",
  },
  pageInfo: {
    fontSize: 16,
    color: "#000000",
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    justifyContent: "flex-end",
  },
  modalContent: {
    backgroundColor: "#ffffff",
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    padding: 24,
    maxHeight: "80%",
  },
  modalHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 24,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#000000",
  },
  filterSection: {
    marginBottom: 24,
  },
  filterLabel: {
    fontSize: 16,
    fontWeight: "600",
    color: "#000000",
    marginBottom: 12,
  },
  priceInputs: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },
  priceInput: {
    flex: 1,
    backgroundColor: "#f5f5f5",
    padding: 12,
    borderRadius: 8,
    fontSize: 16,
  },
  priceSeparator: {
    fontSize: 18,
    color: "#666666",
  },
  availabilityButtons: {
    flexDirection: "row",
    gap: 8,
  },
  availabilityButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#e0e0e0",
    alignItems: "center",
  },
  availabilityButtonActive: {
    backgroundColor: "#000000",
    borderColor: "#000000",
  },
  availabilityButtonText: {
    fontSize: 14,
    fontWeight: "600",
    color: "#000000",
  },
  availabilityButtonTextActive: {
    color: "#ffffff",
  },
  modalActions: {
    flexDirection: "row",
    gap: 12,
    marginTop: 24,
  },
  clearButton: {
    flex: 1,
    paddingVertical: 16,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#000000",
    alignItems: "center",
  },
  clearButtonText: {
    fontSize: 16,
    fontWeight: "600",
    color: "#000000",
  },
  applyButton: {
    flex: 1,
    paddingVertical: 16,
    borderRadius: 8,
    backgroundColor: "#000000",
    alignItems: "center",
  },
  applyButtonText: {
    fontSize: 16,
    fontWeight: "600",
    color: "#ffffff",
  },
});