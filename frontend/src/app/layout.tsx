import type { Metadata } from "next";
import { ColorSchemeScript, MantineProvider, createTheme } from "@mantine/core";
import "./globals.css";
import { Providers } from "./providers";

const theme = createTheme({ fontFamily: "Inter, sans-serif" });

export const metadata: Metadata = {
  title: "Hackathon App",
  description: "Built with Django + Next.js boilerplate",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <ColorSchemeScript />
      </head>
      <body>
        <MantineProvider theme={theme}>
          <Providers>{children}</Providers>
        </MantineProvider>
      </body>
    </html>
  );
}
