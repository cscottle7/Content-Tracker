"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import Link from "next/link"
import { api } from "@/lib/api"
import { ContentItem } from "@/lib/types"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

export function ContentList() {
  const searchParams = useSearchParams()
  const [content, setContent] = useState<ContentItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [pagination, setPagination] = useState({ page: 1, per_page: 50, total: 0, pages: 0 })

  useEffect(() => {
    async function fetchContent() {
      try {
        setLoading(true)

        // Build filter object from search params
        const filters: any = {}
        searchParams.forEach((value, key) => {
          if (key !== "page" && key !== "per_page") {
            filters[key] = value
          }
        })

        const page = parseInt(searchParams.get("page") || "1")
        const per_page = parseInt(searchParams.get("per_page") || "50")

        const data = await api.content.list(filters, page, per_page)
        setContent(data.items || [])
        setPagination(data.pagination || { page: 1, per_page: 50, total: 0, pages: 0 })
        setError(null)
      } catch (err) {
        console.error("Failed to fetch content:", err)
        setError(err instanceof Error ? err.message : "Failed to load content")
        setContent([])
      } finally {
        setLoading(false)
      }
    }

    fetchContent()
  }, [searchParams])

  if (loading) {
    return <div className="text-center py-12">Loading content...</div>
  }

  if (error) {
    return (
      <div className="text-center py-12 bg-red-50 rounded-lg p-4">
        <p className="text-red-600 mb-4">{error}</p>
        <Button onClick={() => window.location.reload()}>Retry</Button>
      </div>
    )
  }

  if (content.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <p className="text-gray-600 mb-4">
          No content found. {searchParams.toString() ? "Try adjusting your filters." : "Create your first item to get started."}
        </p>
        {!searchParams.toString() && (
          <Link href="/content/new">
            <Button>Create Content</Button>
          </Link>
        )}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="bg-white shadow-sm rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Title
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Updated
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Tags
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {content.map((item) => (
              <tr key={item.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <Link
                    href={`/content/${item.id}`}
                    className="text-blue-600 hover:underline font-medium"
                  >
                    {item.title}
                  </Link>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="text-sm text-gray-900">{item.content_type}</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <Badge variant={item.status === "published" ? "default" : "secondary"}>
                    {item.status}
                  </Badge>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(item.updated_date).toLocaleDateString()}
                </td>
                <td className="px-6 py-4">
                  <div className="flex gap-1 flex-wrap">
                    {item.tags.slice(0, 3).map((tag) => (
                      <Badge key={tag} variant="outline" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                    {item.tags.length > 3 && (
                      <Badge variant="outline" className="text-xs">
                        +{item.tags.length - 3}
                      </Badge>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {pagination.pages > 1 && (
        <div className="flex justify-between items-center mt-4">
          <div className="text-sm text-gray-500">
            Showing {(pagination.page - 1) * pagination.per_page + 1} to{" "}
            {Math.min(pagination.page * pagination.per_page, pagination.total)} of {pagination.total} results
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={pagination.page <= 1}
              onClick={() => {
                const params = new URLSearchParams(searchParams.toString())
                params.set("page", String(pagination.page - 1))
                window.location.href = `/content?${params.toString()}`
              }}
            >
              Previous
            </Button>
            <Button
              variant="outline"
              size="sm"
              disabled={pagination.page >= pagination.pages}
              onClick={() => {
                const params = new URLSearchParams(searchParams.toString())
                params.set("page", String(pagination.page + 1))
                window.location.href = `/content?${params.toString()}`
              }}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
