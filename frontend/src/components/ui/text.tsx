import * as React from "react"
import { cn } from "@/lib/utils"

type TextVariant = "default" | "muted" | "secondary" | "small" | "lead"

interface TextProps extends React.HTMLAttributes<HTMLParagraphElement> {
  variant?: TextVariant
  as?: "p" | "span" | "div" | "label"
}

const variantClasses: Record<TextVariant, string> = {
  default: "text-base text-foreground",
  muted: "text-sm text-muted-foreground",
  secondary: "text-sm text-muted-foreground",
  small: "text-xs text-muted-foreground",
  lead: "text-lg text-foreground",
}

function Text({
  as: Tag = "p",
  variant = "default",
  className,
  children,
  ...props
}: TextProps) {
  return (
    <Tag
      className={cn(
        "font-sans leading-relaxed",
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {children}
    </Tag>
  )
}

export { Text }
