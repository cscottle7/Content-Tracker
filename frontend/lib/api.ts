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

  // Content endpoints
  content: {
    list: async (filters?: any, page = 1, perPage = 50) => {
      const queryParams = new URLSearchParams()
      queryParams.set("page", page.toString())
      queryParams.set("per_page", perPage.toString())

      // Add all filter parameters
      if (filters) {
        Object.keys(filters).forEach((key) => {
          if (filters[key]) {
            queryParams.set(key, filters[key])
          }
        })
      }

      return apiFetch<{
        items: any[]
        pagination: {
          page: number
          per_page: number
          total: number
          pages: number
        }
      }>(`/content?${queryParams}`)
    },

    get: (id: string) => apiFetch<any>(`/content/${id}`),

    create: (data: any) =>
      apiFetch<any>("/content", {
        method: "POST",
        body: JSON.stringify(data),
      }),

    update: (id: string, data: any) =>
      apiFetch<any>(`/content/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),

    delete: (id: string) =>
      apiFetch<void>(`/content/${id}`, {
        method: "DELETE",
      }),
  },
}

export default api
