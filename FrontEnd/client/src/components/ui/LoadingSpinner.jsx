import { cn } from '../../lib/utils';

const LoadingSpinner = ({ className, size = 'md' }) => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16'
  };

  return (
    <div
      className={cn(
        'animate-spin rounded-full border-2 border-gray-300 border-t-green-600',
        sizes[size],
        className
      )}
    />
  );
};

export default LoadingSpinner;