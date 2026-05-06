import { Component, ReactNode, ErrorInfo } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export default class LalKitabErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error, errorInfo: null };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    if (import.meta.env.DEV) {
      console.error('❌ LalKitab Error Boundary caught:', error.message);
      console.error('Error Info:', errorInfo);
      console.log('Component Stack:', errorInfo.componentStack);

      // Log specifically for React Error #31 (bilingual object rendering)
      if (error.message.includes('with keys')) {
        console.error('⚠️  REACT ERROR #31 - Bilingual object render attempt detected');
        console.error('This means somewhere we\'re trying to render {hi: "...", en: "..."} directly');
        console.error('Stack:', errorInfo.componentStack);
      }
    }

    this.setState({ errorInfo });
  }

  render() {
    if (this.state.hasError) {
      const hi = typeof document !== 'undefined' && document.documentElement.lang === 'hi';
      return (
        <div className="p-6 bg-red-50 border-2 border-red-300 rounded-xl">
          <h2 className="text-xl font-bold text-red-700 mb-2">{hi ? 'कुछ गलत हुआ' : 'Something went wrong'}</h2>
          <p className="text-sm text-red-600 mb-3">{this.state.error?.message}</p>
          {this.state.errorInfo && (
            <details className="text-xs text-red-700 bg-white p-3 rounded border border-red-200">
              <summary className="cursor-pointer font-mono font-bold">{hi ? 'त्रुटि विवरण' : 'Error Details'}</summary>
              <pre className="mt-2 overflow-x-auto whitespace-pre-wrap">
                {this.state.errorInfo.componentStack}
              </pre>
            </details>
          )}
          <button
            onClick={() => window.location.reload()}
            className="mt-3 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            {hi ? 'पेज रीलोड करें' : 'Reload Page'}
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
