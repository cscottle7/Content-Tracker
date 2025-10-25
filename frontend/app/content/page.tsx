"use client"

import { Suspense } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { SearchBar } from "@/components/SearchBar"
import { FilterPanel } from "@/components/FilterPanel"
import { ContentList } from "@/components/ContentList"

export default function ContentListPage() {
  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Content Library</h1>
        <Link href="/content/new">
          <Button>Add Content</Button>
        </Link>
      </div>

      <div className="mb-6">
        <SearchBar />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <aside className="lg:col-span-1">
          <FilterPanel />
        </aside>
        <div className="lg:col-span-3">
          <Suspense fallback={<div className="text-center py-12">Loading...</div>}>
            <ContentList />
          </Suspense>
        </div>
      </div>
    </div>
  )
}
