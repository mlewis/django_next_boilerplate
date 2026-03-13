"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

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
    <main className="container mx-auto py-12 px-4">
      <div className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight">Hackathon Boilerplate</h1>
        <p className="mt-2 text-muted-foreground">
          Django Ninja + Next.js + Tailwind + shadcn + TanStack Query
        </p>
      </div>

      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Items</CardTitle>
          <CardDescription>
            Fetched from <code className="text-xs bg-muted px-1 py-0.5 rounded">/api/items/</code>{" "}
            via TanStack Query with fully typed{" "}
            <code className="text-xs bg-muted px-1 py-0.5 rounded">openapi-fetch</code>
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading && <p className="text-muted-foreground">Loading...</p>}
          {isError && (
            <p className="text-destructive">
              Could not load items — make sure the backend is running and you are authenticated.
            </p>
          )}
          {items && items.length === 0 && (
            <p className="text-muted-foreground">No items yet. Create one via the API.</p>
          )}
          {items && items.length > 0 && (
            <ul className="space-y-3">
              {items.map((item) => (
                <li key={item.id} className="flex items-center gap-3 rounded-md border p-3">
                  <span className="flex-1 font-medium">{item.title}</span>
                  <Badge variant={item.completed ? "default" : "secondary"}>
                    {item.completed ? "Done" : "Pending"}
                  </Badge>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-3 text-sm text-muted-foreground">
        <div className="rounded-md border p-4">
          <p className="font-semibold text-foreground mb-1">API Docs</p>
          <a href="/api/docs" className="text-primary hover:underline">
            /api/docs →
          </a>
        </div>
        <div className="rounded-md border p-4">
          <p className="font-semibold text-foreground mb-1">OpenAPI Schema</p>
          <a href="/api/openapi.json" className="text-primary hover:underline">
            /api/openapi.json →
          </a>
        </div>
        <div className="rounded-md border p-4">
          <p className="font-semibold text-foreground mb-1">Admin</p>
          <a href="/admin/" className="text-primary hover:underline">
            /admin/ →
          </a>
        </div>
      </div>
    </main>
  );
}
