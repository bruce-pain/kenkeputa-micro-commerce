import AsyncStorage from "@react-native-async-storage/async-storage";

const TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";
const USER_KEY = "user_data";

export const storage = {
  async saveTokens(accessToken: string, refreshToken: string) {
    await AsyncStorage.multiSet([
      [TOKEN_KEY, accessToken],
      [REFRESH_TOKEN_KEY, refreshToken],
    ]);
  },

  async getAccessToken() {
    return await AsyncStorage.getItem(TOKEN_KEY);
  },

  async getRefreshToken() {
    return await AsyncStorage.getItem(REFRESH_TOKEN_KEY);
  },

  async saveUser(userData: any) {
    await AsyncStorage.setItem(USER_KEY, JSON.stringify(userData));
  },

  async getUser() {
    const user = await AsyncStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
  },

  async clearAll() {
    await AsyncStorage.multiRemove([TOKEN_KEY, REFRESH_TOKEN_KEY, USER_KEY]);
  },
};