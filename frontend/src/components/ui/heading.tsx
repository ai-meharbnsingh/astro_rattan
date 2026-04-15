import * as React from "react"
import { cn } from "@/lib/utils"

type HeadingLevel = 1 | 2 | 3 | 4 | 5 | 6

interface HeadingProps extends React.HTMLAttributes<HTMLHeadingElement> {
  as?: HeadingLevel
  variant?: HeadingLevel
}

const variantClasses: Record<HeadingLevel, string> = {
  1: "text-3xl md:text-4xl font-semibold tracking-tight",
  2: "text-2xl md:text-3xl font-semibold tracking-tight",
  3: "text-xl md:text-2xl font-semibold tracking-tight",
  4: "text-lg md:text-xl font-semibold tracking-tight",
  5: "text-base md:text-lg font-semibold",
  6: "text-sm md:text-base font-semibold",
}

function Heading({
  as = 1,
  variant,
  className,
  children,
  ...props
}: HeadingProps) {
  const Tag = `h${as}` as React.ElementType
  const v = variant ?? as
  return (
    <Tag
      className={cn(
        "text-foreground font-sans",
        variantClasses[v],
        className
      )}
      {...props}
    >
      {children}
    </Tag>
  )
}

export { Heading }
