import React, { useState } from 'react'
import axios from 'axios'
import { Toaster, toast } from 'react-hot-toast'
import Plot from 'react-plotly.js'

const API_URL = 'http://localhost:8000'

function App() {
  const [ticker, setTicker] = useState('AAPL')
  const [stockData, setStockData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [queryLoading, setQueryLoading] = useState(false)

  const analyzeStock = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_URL}/api/stocks/${ticker}`)
      setStockData(response.data)
      toast.success(`Loaded ${ticker} data!`)
    } catch (error) {
      toast.error('Failed to load stock data')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const askQuestion = async () => {
    if (!question.trim()) return
    
    setQueryLoading(true)
    setAnswer('')
    
    try {
      const response = await axios.post(`${API_URL}/api/queries/`, {
        question: question,
        user_id: 'user1'
      })
      
      const queryId = response.data.query_id
      
      // Poll for results
      const pollInterval = setInterval(async () => {
        const result = await axios.get(`${API_URL}/api/queries/${queryId}`)
        
        if (result.data.status === 'completed') {
          setAnswer(result.data.answer)
          setQueryLoading(false)
          clearInterval(pollInterval)
          toast.success('Analysis complete!')
        } else if (result.data.status === 'failed') {
          setAnswer('Failed to process your question.')
          setQueryLoading(false)
          clearInterval(pollInterval)
          toast.error('Analysis failed')
        }
      }, 1000)
      
    } catch (error) {
      toast.error('Failed to send question')
      setQueryLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-gray-900/50 backdrop-blur-lg border-b border-gray-700">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-green-400 to-blue-500 bg-clip-text text-transparent">
                FinMind
              </h1>
              <p className="text-gray-400 mt-1">Financial Intelligence System</p>
            </div>
            <div className="text-sm text-gray-400">
              🟢 System Online
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Stock Analysis */}
          <div className="space-y-6">
            {/* Stock Search */}
            <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-gray-700">
              <h2 className="text-xl font-semibold text-white mb-4">Stock Analysis</h2>
              <div className="flex gap-2 mb-4">
                <input
                  type="text"
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value.toUpperCase())}
                  placeholder="Enter ticker (e.g., AAPL)"
                  className="flex-1 bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-green-500"
                />
                <button
                  onClick={analyzeStock}
                  disabled={loading}
                  className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors disabled:opacity-50"
                >
                  {loading ? 'Loading...' : 'Analyze'}
                </button>
              </div>
              
              {stockData && (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-700/50 rounded-lg p-3">
                      <div className="text-gray-400 text-sm">Price</div>
                      <div className="text-2xl font-bold text-white">
                        ${stockData.current_price}
                      </div>
                      <div className={stockData.price_change >= 0 ? 'text-green-400' : 'text-red-400'}>
                        {stockData.price_change >= 0 ? '↑' : '↓'} {Math.abs(stockData.price_change)}%
                      </div>
                    </div>
                    <div className="bg-gray-700/50 rounded-lg p-3">
                      <div className="text-gray-400 text-sm">Market Cap</div>
                      <div className="text-xl font-bold text-white">
                        ${(stockData.market_cap / 1e9).toFixed(1)}B
                      </div>
                    </div>
                    <div className="bg-gray-700/50 rounded-lg p-3">
                      <div className="text-gray-400 text-sm">P/E Ratio</div>
                      <div className="text-xl font-bold text-white">
                        {stockData.pe_ratio}
                      </div>
                    </div>
                    <div className="bg-gray-700/50 rounded-lg p-3">
                      <div className="text-gray-400 text-sm">Volume</div>
                      <div className="text-xl font-bold text-white">
                        {(stockData.volume / 1e6).toFixed(1)}M
                      </div>
                    </div>
                  </div>
                  
                  {/* Price Chart */}
                  {stockData.chart_data && (
                    <Plot
                      data={[
                        {
                          x: stockData.chart_data.dates,
                          y: stockData.chart_data.prices,
                          type: 'scatter',
                          mode: 'lines',
                          name: 'Price',
                          line: { color: '#10b981', width: 2 }
                        }
                      ]}
                      layout={{
                        title: `${stockData.name} (${stockData.ticker})`,
                        template: 'plotly_dark',
                        height: 400,
                        margin: { t: 40, r: 20, b: 30, l: 50 },
                        paper_bgcolor: 'rgba(0,0,0,0)',
                        plot_bgcolor: 'rgba(0,0,0,0)'
                      }}
                      useResizeHandler={true}
                      style={{ width: '100%', height: '400px' }}
                    />
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Right Column - AI Assistant */}
          <div className="space-y-6">
            <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-gray-700">
              <h2 className="text-xl font-semibold text-white mb-4">AI Financial Assistant</h2>
              
              <div className="space-y-4">
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask any financial question... (e.g., 'How is Apple performing?', 'Should I invest in Microsoft?')"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-green-500 min-h-[100px]"
                />
                
                <button
                  onClick={askQuestion}
                  disabled={queryLoading || !question.trim()}
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white py-3 rounded-lg font-semibold transition-all disabled:opacity-50"
                >
                  {queryLoading ? 'Analyzing...' : 'Ask AI Assistant'}
                </button>
                
                {answer && (
                  <div className="mt-6 p-4 bg-gray-700/30 rounded-lg border border-gray-600">
                    <div className="text-purple-400 font-semibold mb-2">AI Response:</div>
                    <div className="text-gray-200 whitespace-pre-wrap">{answer}</div>
                  </div>
                )}
              </div>
            </div>
            
            {/* Quick Tips */}
            <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-gray-700">
              <h3 className="text-lg font-semibold text-white mb-3">💡 Quick Questions</h3>
              <div className="space-y-2">
                {[
                  "How is Apple (AAPL) performing?",
                  "What's the outlook for Microsoft (MSFT)?",
                  "Analyze Nvidia's (NVDA) growth",
                  "Should I invest in Tesla (TSLA)?"
                ].map((q, i) => (
                  <button
                    key={i}
                    onClick={() => setQuestion(q)}
                    className="w-full text-left px-3 py-2 bg-gray-700/50 hover:bg-gray-700 rounded-lg text-gray-300 text-sm transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App