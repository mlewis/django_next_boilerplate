"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import {
  Anchor,
  Badge,
  Card,
  Container,
  Group,
  SimpleGrid,
  Stack,
  Text,
  Title,
} from "@mantine/core";

async function fetchItems() {
  const { data, error } = await apiClient.GET("/api/items/");
  if (error) throw new Error("Failed to fetch items");
  return data;
}

export default function HomePage() {
  const { data: items, isLoading, isError } = useQuery({
    queryKey: ["items"],
    queryFn: fetchItems,
  });

  return (
    <Container py="xl">
      <Stack mb="xl" gap="xs">
        <Title order={1}>Hackathon Boilerplate</Title>
        <Text c="dimmed">Django Ninja + Next.js + Mantine + TanStack Query</Text>
      </Stack>

      <Card withBorder shadow="sm" radius="md" mb="lg">
        <Stack gap="xs" mb="md">
          <Text fw={600} size="xl">Items</Text>
          <Text size="sm" c="dimmed">
            Fetched from <Text component="code" size="xs" bg="gray.1" px={4} py={2} style={{ borderRadius: 4 }}>/api/items/</Text>{" "}
            via TanStack Query with fully typed{" "}
            <Text component="code" size="xs" bg="gray.1" px={4} py={2} style={{ borderRadius: 4 }}>openapi-fetch</Text>
          </Text>
        </Stack>

        {isLoading && <Text c="dimmed">Loading...</Text>}
        {isError && (
          <Text c="red">
            Could not load items — make sure the backend is running and you are authenticated.
          </Text>
        )}
        {items && items.length === 0 && (
          <Text c="dimmed">No items yet. Create one via the API.</Text>
        )}
        {items && items.length > 0 && (
          <Stack gap="sm">
            {items.map((item) => (
              <Group
                key={item.id}
                justify="space-between"
                p="sm"
                style={{ border: "1px solid var(--mantine-color-gray-3)", borderRadius: "var(--mantine-radius-md)" }}
              >
                <Text fw={500}>{item.title}</Text>
                <Badge color={item.completed ? "green" : "gray"}>
                  {item.completed ? "Done" : "Pending"}
                </Badge>
              </Group>
            ))}
          </Stack>
        )}
      </Card>

      <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="md">
        {[
          { label: "API Docs", href: "/api/docs", linkText: "/api/docs →" },
          { label: "OpenAPI Schema", href: "/api/openapi.json", linkText: "/api/openapi.json →" },
          { label: "Admin", href: "/admin/", linkText: "/admin/ →" },
        ].map(({ label, href, linkText }) => (
          <Card key={href} withBorder p="md">
            <Text fw={600} mb={4}>{label}</Text>
            <Anchor href={href} size="sm">{linkText}</Anchor>
          </Card>
        ))}
      </SimpleGrid>
    </Container>
  );
}
