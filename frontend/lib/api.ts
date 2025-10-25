/**
 * API client for Content Tracking System backend.
 *
 * Provides typed functions for all API endpoints.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

/**
 * Generic fetch wrapper with error handling.
 */
async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_URL}${endpoint}`

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      message: "An error occurred",
    }))
    throw new Error(error.message || `HTTP ${response.status}`)
  }

  return response.json()
}

/**
 * API client object with all endpoints.
 */
export const api = {
  // Health check
  health: () => apiFetch<{ status: string }>("/health"),

  // Content endpoints (to be implemented)
  content: {
    list: async (params?: {
      page?: number
      pageSize?: number
      contentType?: string
      status?: string
    }) => {
      const queryParams = new URLSearchParams()
      if (params?.page) queryParams.set("page", params.page.toString())
      if (params?.pageSize)
        queryParams.set("page_size", params.pageSize.toString())
      if (params?.contentType)
        queryParams.set("content_type", params.contentType)
      if (params?.status) queryParams.set("status", params.status)

      return apiFetch<any>(`/api/content?${queryParams}`)
    },

    get: (id: string) => apiFetch<any>(`/api/content/${id}`),

    create: (data: any) =>
      apiFetch<any>("/api/content", {
        method: "POST",
        body: JSON.stringify(data),
      }),

    update: (id: string, data: any) =>
      apiFetch<any>(`/api/content/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),

    delete: (id: string) =>
      apiFetch<void>(`/api/content/${id}`, {
        method: "DELETE",
      }),
  },
}

export default api
