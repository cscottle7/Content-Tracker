"use client"

import { useEffect, useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

const CONTENT_TYPES = ["blog", "video", "podcast", "social", "research"]
const STATUSES = ["draft", "published", "archived"]

export function FilterPanel() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [clients, setClients] = useState<string[]>([])

  useEffect(() => {
    async function fetchClients() {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/search/filters`)
        const data = await response.json()
        setClients(data.clients || [])
      } catch (err) {
        console.error("Failed to fetch clients:", err)
      }
    }
    fetchClients()
  }, [])

  function updateFilter(key: string, value: string | null) {
    const params = new URLSearchParams(searchParams.toString())
    if (value) {
      params.set(key, value)
    } else {
      params.delete(key)
    }
    router.push(`/content?${params.toString()}`)
  }

  function clearAllFilters() {
    router.push("/content")
  }

  const activeFilters = Array.from(searchParams.entries()).filter(
    ([key]) => key !== "page" && key !== "per_page"
  )

  return (
    <div className="space-y-4 p-4 border rounded-lg bg-white shadow-sm">
      <div className="flex justify-between items-center">
        <h3 className="font-semibold text-lg">Filters</h3>
        {activeFilters.length > 0 && (
          <Button variant="ghost" size="sm" onClick={clearAllFilters}>
            Clear All
          </Button>
        )}
      </div>

      {activeFilters.length > 0 && (
        <div className="flex flex-wrap gap-2 pb-4 border-b">
          {activeFilters.map(([key, value]) => (
            <Badge key={`${key}-${value}`} variant="secondary" className="flex items-center gap-1">
              <span className="text-xs">
                {key}: {value}
              </span>
              <button
                onClick={() => updateFilter(key, null)}
                className="ml-1 hover:bg-gray-600 rounded-full p-0.5"
                aria-label={`Remove ${key} filter`}
              >
                <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </Badge>
          ))}
        </div>
      )}

      <div className="space-y-4">
        <div>
          <Label htmlFor="content_type" className="text-sm font-medium mb-2 block">
            Content Type
          </Label>
          <select
            id="content_type"
            value={searchParams.get("content_type") || ""}
            onChange={(e) => updateFilter("content_type", e.target.value || null)}
            className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
          >
            <option value="">All types</option>
            {CONTENT_TYPES.map((type) => (
              <option key={type} value={type}>
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <Label htmlFor="status" className="text-sm font-medium mb-2 block">
            Status
          </Label>
          <select
            id="status"
            value={searchParams.get("status") || ""}
            onChange={(e) => updateFilter("status", e.target.value || null)}
            className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
          >
            <option value="">All statuses</option>
            {STATUSES.map((status) => (
              <option key={status} value={status}>
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <Label htmlFor="client" className="text-sm font-medium mb-2 block">
            Client
          </Label>
          <select
            id="client"
            value={searchParams.get("client") || ""}
            onChange={(e) => updateFilter("client", e.target.value || null)}
            className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
          >
            <option value="">All clients</option>
            {clients.map((client) => (
              <option key={client} value={client}>
                {client}
              </option>
            ))}
          </select>
        </div>

        <div>
          <Label htmlFor="date_from" className="text-sm font-medium mb-2 block">
            From Date
          </Label>
          <input
            type="date"
            id="date_from"
            value={searchParams.get("date_from") || ""}
            onChange={(e) => updateFilter("date_from", e.target.value || null)}
            className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
          />
        </div>

        <div>
          <Label htmlFor="date_to" className="text-sm font-medium mb-2 block">
            To Date
          </Label>
          <input
            type="date"
            id="date_to"
            value={searchParams.get("date_to") || ""}
            onChange={(e) => updateFilter("date_to", e.target.value || null)}
            className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
          />
        </div>
      </div>

      <div className="pt-4 border-t text-xs text-gray-500">
        <p>Filter by multiple criteria to narrow your search</p>
      </div>
    </div>
  )
}
