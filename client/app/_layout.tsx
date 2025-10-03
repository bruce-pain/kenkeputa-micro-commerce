import { Stack } from "expo-router";

export default function RootLayout() {
    return (
        <Stack>
            <Stack.Screen name="splash" options={{ headerShown: false }} />
            <Stack.Screen
                name="auth/login"
                options={{ title: "Login", headerShown: false }}
            />
            <Stack.Screen
                name="auth/register"
                options={{ title: "Register", headerShown: false }}  
            />
            <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        </Stack>
    );
}
