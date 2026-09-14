// 统一头像渲染：avatar 字段可能是 emoji（短字符串）或 base64 图片（data:image/...）
export function isImageAvatar(v?: string) {
  return !!v && v.startsWith('data:image/')
}

export default function UserAvatar({
  value,
  className = '',
  imgClassName = '',
}: {
  value?: string
  /** emoji 模式下的字体大小类，如 text-lg */
  className?: string
  /** 图片模式下的尺寸类，如 h-6 w-6；默认 h-[1.2em] w-[1.2em] 随字体 */
  imgClassName?: string
}) {
  if (isImageAvatar(value)) {
    return (
      <img
        src={value}
        alt="头像"
        className={`inline-block shrink-0 rounded-full object-cover align-middle ${imgClassName || 'h-[1.25em] w-[1.25em]'} ${className}`}
      />
    )
  }
  return <span className={className}>{value || '🧪'}</span>
}
