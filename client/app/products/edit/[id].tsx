import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { useState, useEffect } from "react";
import { useRouter, useLocalSearchParams } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { apiService } from "@/services/api";
import { ApiError } from "@/types/auth";

export default function EditProduct() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [stock, setStock] = useState("");

  useEffect(() => {
    loadProduct();
  }, [id]);

  const loadProduct = async () => {
    if (!id) return;

    try {
      const response = await apiService.getProduct(id);
      const product = response.data;
      setName(product.name);
      setDescription(product.description || "");
      setPrice(parseFloat(product.price.toString()).toFixed(2));
      setStock(product.stock.toString());
    } catch (error) {
      const apiError = error as ApiError;
      Alert.alert("Error", apiError.message || "Failed to load product");
      router.back();
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    if (!name) {
      Alert.alert("Error", "Product name is required");
      return;
    }

    const updateData: any = {};

    if (name) updateData.name = name;
    if (description) updateData.description = description;
    if (price) {
      const priceValue = parseFloat(price);
      if (isNaN(priceValue) || priceValue <= 0) {
        Alert.alert("Error", "Please enter a valid price");
        return;
      }
      updateData.price = priceValue;
    }
    if (stock) {
      const stockValue = parseInt(stock, 10);
      if (isNaN(stockValue) || stockValue < 0) {
        Alert.alert("Error", "Please enter a valid stock quantity");
        return;
      }
      updateData.stock = stockValue;
    }

    setSubmitting(true);
    try {
      const response = await apiService.updateProduct(id!, updateData);
      Alert.alert("Success", response.message);
      router.back();
    } catch (error) {
      const apiError = error as ApiError;
      Alert.alert("Error", apiError.message || "Failed to update product");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#000000" />
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      style={styles.container}
    >
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#000000" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Edit Product</Text>
        <View style={styles.headerSpacer} />
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.form}>
          <View style={styles.formGroup}>
            <Text style={styles.label}>
              Product Name <Text style={styles.required}>*</Text>
            </Text>
            <TextInput
              style={styles.input}
              placeholder="Enter product name"
              value={name}
              onChangeText={setName}
              editable={!submitting}
            />
          </View>

          <View style={styles.formGroup}>
            <Text style={styles.label}>Description</Text>
            <TextInput
              style={[styles.input, styles.textArea]}
              placeholder="Enter product description"
              value={description}
              onChangeText={setDescription}
              multiline
              numberOfLines={4}
              textAlignVertical="top"
              editable={!submitting}
            />
          </View>

          <View style={styles.formGroup}>
            <Text style={styles.label}>Price</Text>
            <View style={styles.priceInputContainer}>
              <Text style={styles.currencySymbol}>$</Text>
              <TextInput
                style={[styles.input, styles.priceInput]}
                placeholder="0.00"
                value={price}
                onChangeText={setPrice}
                keyboardType="decimal-pad"
                editable={!submitting}
              />
            </View>
          </View>

          <View style={styles.formGroup}>
            <Text style={styles.label}>Stock Quantity</Text>
            <TextInput
              style={styles.input}
              placeholder="0"
              value={stock}
              onChangeText={setStock}
              keyboardType="number-pad"
              editable={!submitting}
            />
          </View>

          <TouchableOpacity
            style={[styles.submitButton, submitting && styles.submitButtonDisabled]}
            onPress={handleUpdate}
            disabled={submitting}
          >
            {submitting ? (
              <ActivityIndicator color="#ffffff" />
            ) : (
              <>
                <Ionicons name="save-outline" size={20} color="#ffffff" />
                <Text style={styles.submitButtonText}>Save Changes</Text>
              </>
            )}
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
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
  },
  form: {
    padding: 16,
    gap: 20,
  },
  formGroup: {
    gap: 8,
  },
  label: {
    fontSize: 16,
    fontWeight: "600",
    color: "#000000",
  },
  required: {
    color: "#ff3b30",
  },
  input: {
    backgroundColor: "#ffffff",
    padding: 16,
    borderRadius: 8,
    fontSize: 16,
    borderWidth: 1,
    borderColor: "#e0e0e0",
  },
  textArea: {
    minHeight: 100,
    paddingTop: 16,
  },
  priceInputContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#ffffff",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#e0e0e0",
  },
  currencySymbol: {
    fontSize: 18,
    fontWeight: "600",
    color: "#000000",
    paddingLeft: 16,
  },
  priceInput: {
    flex: 1,
    borderWidth: 0,
  },
  submitButton: {
    flexDirection: "row",
    backgroundColor: "#000000",
    padding: 16,
    borderRadius: 8,
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    marginTop: 24,
  },
  submitButtonDisabled: {
    opacity: 0.6,
  },
  submitButtonText: {
    color: "#ffffff",
    fontSize: 16,
    fontWeight: "600",
  },
});