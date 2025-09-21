// components/ui/spinner.tsx
import React from "react"
import { ReactNode } from "react"

export function Spinner({ className }: { className?: string }) {
  return (
    <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-[#4a43ec]"></div>
  )
}


export function SpinnerWrapper({isLoading, children}: {isLoading:boolean, children: ReactNode}){
  return (
    <div className="relative">
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/70 z-10">
          <Spinner></Spinner>
        </div>
      )}
      {children}
      </div>
  )
}