"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"
import { ContentItem } from "@/lib/types"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

export default function ContentEditPage({ params }: { params: { id: string } }) {
  const [content, setContent] = useState<ContentItem | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    async function fetchContent() {
      try {
        const data = await api.content.get(params.id)
        setContent(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load content")
      } finally {
        setLoading(false)
      }
    }

    fetchContent()
  }, [params.id])

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    if (!content) return

    setSaving(true)
    setError(null)

    try {
      await api.content.update(params.id, content)
      router.push(`/content/${params.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save changes")
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto py-8">
        <div className="text-center py-12">Loading...</div>
      </div>
    )
  }

  if (error && !content) {
    return (
      <div className="container mx-auto py-8">
        <div className="text-center py-12 text-red-600">{error}</div>
      </div>
    )
  }

  if (!content) {
    return (
      <div className="container mx-auto py-8">
        <div className="text-center py-12">Content not found</div>
      </div>
    )
  }

  return (
    <div className="container mx-auto py-8 max-w-4xl">
      <h1 className="text-3xl font-bold mb-8">Edit Content</h1>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-md">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <Label htmlFor="title">Title</Label>
          <Input
            id="title"
            value={content.title}
            onChange={(e) => setContent({ ...content, title: e.target.value })}
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="content_type">Content Type</Label>
            <select
              id="content_type"
              value={content.content_type}
              onChange={(e) =>
                setContent({ ...content, content_type: e.target.value })
              }
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
              value={content.status}
              onChange={(e) => setContent({ ...content, status: e.target.value })}
              className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
            >
              <option value="draft">Draft</option>
              <option value="published">Published</option>
              <option value="archived">Archived</option>
            </select>
          </div>
        </div>

        <div>
          <Label htmlFor="description">Description</Label>
          <Textarea
            id="description"
            value={content.description || ""}
            onChange={(e) =>
              setContent({ ...content, description: e.target.value })
            }
            rows={3}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="author">Author</Label>
            <Input
              id="author"
              value={content.author || ""}
              onChange={(e) => setContent({ ...content, author: e.target.value })}
            />
          </div>

          <div>
            <Label htmlFor="url">URL</Label>
            <Input
              id="url"
              type="url"
              value={content.url || ""}
              onChange={(e) => setContent({ ...content, url: e.target.value })}
            />
          </div>
        </div>

        <div>
          <Label htmlFor="tags">Tags (comma-separated)</Label>
          <Input
            id="tags"
            value={content.tags.join(", ")}
            onChange={(e) =>
              setContent({
                ...content,
                tags: e.target.value
                  .split(",")
                  .map((t) => t.trim())
                  .filter(Boolean),
              })
            }
          />
        </div>

        <div>
          <Label htmlFor="categories">Categories (comma-separated)</Label>
          <Input
            id="categories"
            value={content.categories.join(", ")}
            onChange={(e) =>
              setContent({
                ...content,
                categories: e.target.value
                  .split(",")
                  .map((c) => c.trim())
                  .filter(Boolean),
              })
            }
          />
        </div>

        <div>
          <Label htmlFor="body">Content Body (Markdown)</Label>
          <Textarea
            id="body"
            value={content.body || ""}
            onChange={(e) => setContent({ ...content, body: e.target.value })}
            rows={15}
            className="font-mono text-sm"
          />
        </div>

        <div className="flex gap-4">
          <Button type="submit" disabled={saving}>
            {saving ? "Saving..." : "Save Changes"}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => router.push(`/content/${params.id}`)}
          >
            Cancel
          </Button>
        </div>
      </form>
    </div>
  )
}
