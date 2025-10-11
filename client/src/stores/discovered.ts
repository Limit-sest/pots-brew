import { defineStore } from 'pinia'
import type { Item } from '@/types'

export const useDiscovered = defineStore('discovered', {
  state: () => ({
    discovered: [] as Item[],
  }),
  actions: {
    async getInitial() {
      this.discovered.push(await (await fetch('http://127.0.0.1:8000/initial')).json())
    },
    async getNew(ingredients: Item[]) {
      const response = await fetch('http://127.0.0.1:8000/discover', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ingredients),
      })
      if (response.status === 200) {
        this.discovered.push(await response.json())
      } else {
        throw new Error()
      }
    },
  },
})
