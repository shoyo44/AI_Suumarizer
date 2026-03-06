# Design System

## Color Palette

### Primary Colors
- **Primary**: `#6366f1` (Indigo)
- **Primary Dark**: `#4f46e5`
- **Primary Light**: `#818cf8`
- **Secondary**: `#8b5cf6` (Purple)

### Status Colors
- **Success**: `#10b981` (Green)
- **Danger**: `#ef4444` (Red)
- **Warning**: `#f59e0b` (Amber)

### Background Colors
- **Primary**: `#0f172a` (Dark Navy)
- **Secondary**: `#1e293b` (Slate)
- **Tertiary**: `#334155` (Light Slate)

### Text Colors
- **Primary**: `#f1f5f9` (Almost White)
- **Secondary**: `#cbd5e1` (Light Gray)
- **Muted**: `#94a3b8` (Gray)

### Border
- **Default**: `#334155`

## Typography

### Font Family
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
```

### Font Sizes
- **Small**: `0.75rem` (12px)
- **Body**: `0.875rem` (14px)
- **Base**: `0.95rem` (15.2px)
- **Large**: `1.125rem` (18px)
- **Heading**: `1.25rem` (20px)
- **Title**: `1.5rem` (24px)
- **Hero**: `2rem` (32px)

### Font Weights
- **Normal**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700

## Spacing

### Border Radius
- **Small**: `0.375rem` (6px)
- **Medium**: `0.5rem` (8px)
- **Large**: `0.75rem` (12px)
- **XL**: `1rem` (16px)

### Shadows
- **Small**: `0 1px 2px 0 rgb(0 0 0 / 0.05)`
- **Medium**: `0 4px 6px -1px rgb(0 0 0 / 0.1)`
- **Large**: `0 10px 15px -3px rgb(0 0 0 / 0.1)`
- **XL**: `0 20px 25px -5px rgb(0 0 0 / 0.1)`

## Components

### Buttons

#### Primary Button
```css
background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
color: white;
padding: 0.75rem 1.5rem;
border-radius: 0.5rem;
font-weight: 600;
```

**States**:
- Hover: `transform: translateY(-2px)` + shadow
- Active: `transform: translateY(0)`
- Disabled: `opacity: 0.6`

#### Secondary Button
```css
background: #334155;
color: #f1f5f9;
padding: 0.75rem 1.5rem;
border-radius: 0.5rem;
font-weight: 600;
```

### Cards

```css
background: #1e293b;
border: 1px solid #334155;
border-radius: 0.75rem;
padding: 1.5rem;
box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
```

### Inputs

```css
background: #0f172a;
border: 1px solid #334155;
border-radius: 0.5rem;
color: #f1f5f9;
padding: 0.75rem;
transition: border-color 0.2s ease;
```

**Focus State**:
```css
border-color: #6366f1;
```

### Badges

```css
background: rgba(99, 102, 241, 0.1);
border: 1px solid rgba(99, 102, 241, 0.3);
border-radius: 0.5rem;
color: #818cf8;
padding: 0.5rem 1rem;
font-size: 0.875rem;
font-weight: 600;
```

## Animations

### Spin (Loading)
```css
@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### Pulse (Background)
```css
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}
```

### Transitions
- **Default**: `all 0.2s ease`
- **Border**: `border-color 0.2s ease`
- **Color**: `color 0.2s ease`

## Layout

### Container
```css
max-width: 1400px;
margin: 0 auto;
padding: 2rem;
```

### Grid (Analyzer)
```css
display: grid;
grid-template-columns: 1fr 1fr;
gap: 2rem;
```

### Grid (History)
```css
display: grid;
grid-template-columns: 400px 1fr;
gap: 2rem;
```

## Responsive Breakpoints

### Mobile
```css
@media (max-width: 768px) {
  /* Single column layouts */
  /* Hide secondary info */
  /* Reduce padding */
}
```

### Tablet
```css
@media (max-width: 1024px) {
  /* Stack grids */
  /* Adjust spacing */
}
```

## Accessibility

### Focus States
All interactive elements have visible focus states using the primary color.

### Color Contrast
All text meets WCAG AA standards for contrast ratio:
- Primary text on dark background: 15.8:1
- Secondary text on dark background: 9.2:1
- Muted text on dark background: 5.1:1

### Keyboard Navigation
- Tab order follows visual flow
- All buttons and inputs are keyboard accessible
- Focus indicators are clearly visible

## Icons

Using inline SVG icons with:
- **Stroke Width**: 2px
- **Size**: 16px, 20px, 24px, 48px, 64px
- **Color**: Inherits from parent

## Scrollbars

### Custom Scrollbar
```css
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #1e293b;
}

::-webkit-scrollbar-thumb {
  background: #334155;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #334155;
}
```

## Gradients

### Primary Gradient
```css
background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
```

### Background Gradient
```css
background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
```

### Text Gradient
```css
background: linear-gradient(135deg, #818cf8 0%, #8b5cf6 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
```

## Best Practices

1. **Consistency**: Use CSS variables for all colors and spacing
2. **Performance**: Use `transform` for animations instead of position properties
3. **Accessibility**: Always include focus states and proper contrast
4. **Responsiveness**: Mobile-first approach with progressive enhancement
5. **Maintainability**: Keep component styles scoped and organized

## Usage Example

```tsx
// Button with primary style
<button className="btn btn-primary">
  Analyze
</button>

// Card container
<div className="card">
  <h2>Title</h2>
  <p>Content</p>
</div>

// Input field
<input 
  type="text" 
  className="text-input"
  placeholder="Enter text..."
/>
```
