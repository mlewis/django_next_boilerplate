/**
 * Typed API client built on openapi-fetch.
 *
 * Types are generated from the Django Ninja OpenAPI schema via:
 *   pnpm generate-types
 *
 * The generated file (src/types/api.d.ts) is committed so CI works
 * without a running backend.
 */

import createClient from "openapi-fetch";
import type { paths } from "@/types/api";

const BASE_URL =
  typeof window === "undefined"
    ? (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000")
    : ""; // use Next.js rewrites on the client

export const apiClient = createClient<paths>({ baseUrl: BASE_URL });

/** Attach a JWT bearer token to all subsequent requests. */
export function setAuthToken(token: string) {
  apiClient.use({
    async onRequest({ request }) {
      request.headers.set("Authorization", `Bearer ${token}`);
      return request;
    },
  });
}
