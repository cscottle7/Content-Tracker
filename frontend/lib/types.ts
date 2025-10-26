/**
 * TypeScript type definitions for Content Tracking System.
 *
 * Mirrors backend Pydantic models for type safety.
 */

export interface ContentItem {
  id: string
  title: string
  content_type: string
  status: string
  description?: string
  author?: string
  client?: string
  url?: string
  publish_date?: string
  created_date: string
  updated_date: string
  categories: string[]
  tags: string[]
  custom_fields: Record<string, any>
  file_path: string
  body?: string
}

export interface ContentListItem {
  id: string
  title: string
  content_type: string
  status: string
  description?: string
  author?: string
  client?: string
  created_date: string
  updated_date: string
  categories: string[]
  tags: string[]
  file_path: string
}

export interface ContentListResponse {
  items: ContentListItem[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface ContentCreate {
  title: string
  content_type: string
  status?: string
  description?: string
  author?: string
  client?: string
  url?: string
  publish_date?: string
  categories?: string[]
  tags?: string[]
  custom_fields?: Record<string, any>
  body?: string
}

export interface ContentUpdate {
  title?: string
  content_type?: string
  status?: string
  description?: string
  author?: string
  client?: string
  url?: string
  publish_date?: string
  categories?: string[]
  tags?: string[]
  custom_fields?: Record<string, any>
  body?: string
}

export interface ContentFilter {
  content_type?: string
  status?: string
  author?: string
  client?: string
  category?: string
  tag?: string
  start_date?: string
  end_date?: string
  search_query?: string
}

export interface FilterOptions {
  content_types?: string[]
  statuses?: string[]
  authors?: string[]
  clients?: string[]
}

export interface User {
  id: string
  email: string
  full_name?: string
  role: string
  created_at: string
  last_login?: string
  is_active: boolean
}
