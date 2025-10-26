"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

export default function NewContentPage() {
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [clients, setClients] = useState<string[]>([])
  const router = useRouter()

  useEffect(() => {
    // Fetch available clients for dropdown
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

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setCreating(true)
    setError(null)

    const formData = new FormData(e.currentTarget)
    const data = {
      title: formData.get("title") as string,
      content_type: formData.get("content_type") as string,
      status: formData.get("status") as string,
      description: formData.get("description") as string,
      author: formData.get("author") as string,
      client: formData.get("client") as string || undefined,
      url: formData.get("url") as string,
      tags: (formData.get("tags") as string)
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean),
      categories: (formData.get("categories") as string)
        .split(",")
        .map((c) => c.trim())
        .filter(Boolean),
      body: formData.get("body") as string,
      custom_fields: {},
    }

    try {
      const created = await api.content.create(data)
      router.push(`/content/${created.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create content")
      setCreating(false)
    }
  }

  return (
    <div className="container mx-auto py-8 max-w-4xl">
      <h1 className="text-3xl font-bold mb-8">Create New Content</h1>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-md">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <Label htmlFor="title">Title *</Label>
          <Input id="title" name="title" required />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="content_type">Content Type *</Label>
            <select
              id="content_type"
              name="content_type"
              required
              className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
            >
              <option value="blog">Blog</option>
              <option value="video">Video</option>
              <option value="podcast">Podcast</option>
              <option value="social">Social Media</option>
              <option value="research">Research</option>
            </select>
          </div>

          <div>
            <Label htmlFor="status">Status</Label>
            <select
              id="status"
              name="status"
              defaultValue="draft"
              className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
            >
              <option value="draft">Draft</option>
              <option value="published">Published</option>
            </select>
          </div>
        </div>

        <div>
          <Label htmlFor="description">Description</Label>
          <Textarea id="description" name="description" rows={3} />
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <Label htmlFor="author">Author</Label>
            <Input id="author" name="author" />
          </div>

          <div>
            <Label htmlFor="client">Client</Label>
            <Input
              id="client"
              name="client"
              list="client-options"
              placeholder="Select or type client name"
            />
            <datalist id="client-options">
              {clients.map((client) => (
                <option key={client} value={client} />
              ))}
            </datalist>
          </div>

          <div>
            <Label htmlFor="url">URL</Label>
            <Input id="url" name="url" type="url" />
          </div>
        </div>

        <div>
          <Label htmlFor="tags">Tags (comma-separated)</Label>
          <Input
            id="tags"
            name="tags"
            placeholder="seo, tutorial, beginner"
          />
        </div>

        <div>
          <Label htmlFor="categories">Categories (comma-separated)</Label>
          <Input
            id="categories"
            name="categories"
            placeholder="Content Marketing, SEO"
          />
        </div>

        <div>
          <Label htmlFor="body">Content Body (Markdown)</Label>
          <Textarea
            id="body"
            name="body"
            rows={15}
            className="font-mono text-sm"
            placeholder="# Heading

Write your content here in markdown format..."
          />
        </div>

        <div className="flex gap-4">
          <Button type="submit" disabled={creating}>
            {creating ? "Creating..." : "Create Content"}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => router.push("/content")}
          >
            Cancel
          </Button>
        </div>
      </form>
    </div>
  )
}
