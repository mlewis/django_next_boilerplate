import { describe, it, expect, vi, beforeEach } from "vitest";

// Mock openapi-fetch before importing the module under test
vi.mock("openapi-fetch", () => {
  const mockGet = vi.fn();
  const mockPost = vi.fn();
  const mockUse = vi.fn();
  return {
    default: vi.fn(() => ({ GET: mockGet, POST: mockPost, use: mockUse })),
  };
});

import createClient from "openapi-fetch";

describe("apiClient", () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it("is created with the correct base URL on the server", async () => {
    // Simulate server environment (no window)
    const originalWindow = global.window;
    // @ts-expect-error — intentionally removing window for SSR simulation
    delete global.window;

    process.env.NEXT_PUBLIC_API_URL = "http://django:8000";
    await import("@/lib/api-client");

    expect(createClient).toHaveBeenCalledWith(
      expect.objectContaining({ baseUrl: "http://django:8000" })
    );

    global.window = originalWindow;
  });

  it("uses empty base URL on the client (relies on Next.js rewrites)", async () => {
    // window is defined in jsdom environment
    await import("@/lib/api-client");

    expect(createClient).toHaveBeenCalledWith(
      expect.objectContaining({ baseUrl: "" })
    );
  });
});
