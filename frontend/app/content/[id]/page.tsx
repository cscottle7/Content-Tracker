"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { api } from "@/lib/api"
import { ContentItem } from "@/lib/types"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export default function ContentDetailPage({ params }: { params: { id: string } }) {
  const [content, setContent] = useState<ContentItem | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    async function fetchContent() {
      try {
        const data = await api.content.get(params.id)
        setContent(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch content")
      } finally {
        setLoading(false)
      }
    }

    fetchContent()
  }, [params.id])

  async function handleDelete() {
    if (!confirm("Are you sure you want to delete this content?")) return

    try {
      await api.content.delete(params.id)
      router.push("/content")
    } catch (err) {
      alert("Failed to delete content")
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto py-8">
        <div className="text-center py-12">Loading...</div>
      </div>
    )
  }

  if (error) {
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
      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">{content.title}</h1>
          <div className="flex gap-2 mb-4">
            <Badge>{content.content_type}</Badge>
            <Badge variant={content.status === "published" ? "default" : "secondary"}>
              {content.status}
            </Badge>
          </div>
        </div>
        <div className="flex gap-2">
          <Link href={`/content/${params.id}/edit`}>
            <Button variant="outline">Edit</Button>
          </Link>
          <Button variant="destructive" onClick={handleDelete}>
            Delete
          </Button>
        </div>
      </div>

      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Metadata</CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-sm font-medium text-gray-500">Author</div>
              <div>{content.author || "Not specified"}</div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-500">Created</div>
              <div>{new Date(content.created_date).toLocaleDateString()}</div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-500">Updated</div>
              <div>{new Date(content.updated_date).toLocaleDateString()}</div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-500">Publish Date</div>
              <div>
                {content.publish_date
                  ? new Date(content.publish_date).toLocaleDateString()
                  : "Not set"}
              </div>
            </div>
            {content.url && (
              <div className="col-span-2">
                <div className="text-sm font-medium text-gray-500">URL</div>
                <a
                  href={content.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {content.url}
                </a>
              </div>
            )}
          </CardContent>
        </Card>

        {content.description && (
          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p>{content.description}</p>
            </CardContent>
          </Card>
        )}

        {content.body && (
          <Card>
            <CardHeader>
              <CardTitle>Content</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose max-w-none">
                <pre className="whitespace-pre-wrap font-sans">{content.body}</pre>
              </div>
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle>Tags & Categories</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <div className="text-sm font-medium mb-2">Tags</div>
                <div className="flex flex-wrap gap-2">
                  {content.tags.map((tag) => (
                    <Badge key={tag} variant="secondary">
                      {tag}
                    </Badge>
                  ))}
                  {content.tags.length === 0 && (
                    <span className="text-gray-500">No tags</span>
                  )}
                </div>
              </div>
              <div>
                <div className="text-sm font-medium mb-2">Categories</div>
                <div className="flex flex-wrap gap-2">
                  {content.categories.map((cat) => (
                    <Badge key={cat} variant="outline">
                      {cat}
                    </Badge>
                  ))}
                  {content.categories.length === 0 && (
                    <span className="text-gray-500">No categories</span>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
