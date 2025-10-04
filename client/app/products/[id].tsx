import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from "react-native";
import { useState, useEffect } from "react";
import { useRouter, useLocalSearchParams } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { apiService } from "@/services/api";
import { Product } from "@/types/product";
import { ApiError } from "@/types/auth";
import { storage } from "@/utils/storage";

export default function ProductDetail() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    checkUserRole();
    loadProduct();
  }, [id]);

  const checkUserRole = async () => {
    const user = await storage.getUser();
    setIsAdmin(user?.role === "admin");
  };

  const loadProduct = async () => {
    if (!id) return;

    try {
      const response = await apiService.getProduct(id);
      setProduct(response.data);
    } catch (error) {
      const apiError = error as ApiError;
      Alert.alert("Error", apiError.message || "Failed to load product");
      router.back();
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = () => {
    Alert.alert(
      "Delete Product",
      "Are you sure you want to delete this product?",
      [
        {
          text: "Cancel",
          style: "cancel",
        },
        {
          text: "Delete",
          style: "destructive",
          onPress: async () => {
            try {
              await apiService.deleteProduct(id!);
              Alert.alert("Success", "Product deleted successfully");
              router.back();
            } catch (error) {
              const apiError = error as ApiError;
              Alert.alert("Error", apiError.message || "Failed to delete product");
            }
          },
        },
      ]
    );
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#000000" />
      </View>
    );
  }

  if (!product) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Product not found</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#000000" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Product Details</Text>
        <View style={styles.headerSpacer} />
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.card}>
          <Text style={styles.productName}>{product.name}</Text>
          
          <View style={styles.priceContainer}>
            <Text style={styles.price}>${parseFloat(product.price.toString()).toFixed(2)}</Text>
            <View
              style={[
                styles.stockBadge,
                product.stock > 0 ? styles.inStock : styles.outOfStock,
              ]}
            >
              <Text style={styles.stockText}>
                {product.stock > 0 ? `${product.stock} in stock` : "Out of stock"}
              </Text>
            </View>
          </View>

          <View style={styles.divider} />

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Description</Text>
            <Text style={styles.description}>
              {product.description || "No description available"}
            </Text>
          </View>

          <View style={styles.divider} />

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Product Information</Text>
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Product ID</Text>
              <Text style={styles.infoValue} numberOfLines={1}>
                {product.id}
              </Text>
            </View>
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Stock Quantity</Text>
              <Text style={styles.infoValue}>{product.stock} units</Text>
            </View>
          </View>
        </View>

        {isAdmin && (
          <View style={styles.adminActions}>
            <TouchableOpacity
              style={styles.editButton}
              onPress={() => router.push(`/products/edit/${id}`)}
            >
              <Ionicons name="create-outline" size={20} color="#ffffff" />
              <Text style={styles.editButtonText}>Edit Product</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.deleteButton} onPress={handleDelete}>
              <Ionicons name="trash-outline" size={20} color="#ffffff" />
              <Text style={styles.deleteButtonText}>Delete Product</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
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
  errorContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  errorText: {
    fontSize: 16,
    color: "#666666",
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
  backButton: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#000000",
  },
  headerSpacer: {
    width: 40,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  card: {
    backgroundColor: "#ffffff",
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  productName: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#000000",
    marginBottom: 16,
  },
  priceContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 16,
  },
  price: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#000000",
  },
  stockBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  inStock: {
    backgroundColor: "#e8f5e9",
  },
  outOfStock: {
    backgroundColor: "#ffebee",
  },
  stockText: {
    fontSize: 14,
    fontWeight: "600",
  },
  divider: {
    height: 1,
    backgroundColor: "#e0e0e0",
    marginVertical: 16,
  },
  section: {
    marginBottom: 8,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#000000",
    marginBottom: 12,
  },
  description: {
    fontSize: 16,
    color: "#666666",
    lineHeight: 24,
  },
  infoRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 8,
  },
  infoLabel: {
    fontSize: 16,
    color: "#666666",
  },
  infoValue: {
    fontSize: 16,
    color: "#000000",
    fontWeight: "600",
    flex: 1,
    textAlign: "right",
    marginLeft: 16,
  },
  adminActions: {
    gap: 12,
    marginBottom: 32,
  },
  editButton: {
    flexDirection: "row",
    backgroundColor: "#000000",
    padding: 16,
    borderRadius: 8,
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
  },
  editButtonText: {
    color: "#ffffff",
    fontSize: 16,
    fontWeight: "600",
  },
  deleteButton: {
    flexDirection: "row",
    backgroundColor: "#ff3b30",
    padding: 16,
    borderRadius: 8,
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
  },
  deleteButtonText: {
    color: "#ffffff",
    fontSize: 16,
    fontWeight: "600",
  },
});