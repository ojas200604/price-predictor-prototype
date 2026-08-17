import React, { useState } from 'react';
import { TrendingUp, Package, Truck, Cloud } from 'lucide-react';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [darkMode, setDarkMode] = useState(false);

  const bgColor = darkMode ? '#0F1C2E' : '#EEF3F8';
  const textColor = darkMode ? '#E8F1FA' : '#0F1E33';
  const cardColor = darkMode ? '#1D2C42' : '#FFFFFF';

  return (
    <div style={{ background: bgColor, minHeight: '100vh', color: textColor, fontFamily: 'Arial, sans-serif' }}>
      {/* Header */}
      <header style={{ background: cardColor, padding: '20px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ margin: 0, fontSize: '24px', fontWeight: 'bold' }}>📊 AgriPrice Intelligence</h1>
            <p style={{ margin: '5px 0 0 0', fontSize: '12px', opacity: 0.7 }}>AI-Enabled Price Prediction</p>
          </div>
          <button
            onClick={() => setDarkMode(!darkMode)}
            style={{
              padding: '8px 16px',
              background: '#0B5FA5',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer'
            }}
          >
            {darkMode ? '☀️ Light' : '🌙 Dark'}
          </button>
        </div>
      </header>

      <div style={{ display: 'flex', maxWidth: '1400px', margin: '0 auto' }}>
        {/* Sidebar */}
        <aside style={{
          width: '250px',
          background: cardColor,
          padding: '20px',
          borderRight: '1px solid #DCE6EF',
          minHeight: 'calc(100vh - 80px)'
        }}>
          <nav>
            {[
              { id: 'dashboard', label: '📈 Dashboard', icon: TrendingUp },
              { id: 'forecast', label: '🔮 Price Forecast', icon: TrendingUp },
              { id: 'transport', label: '🚚 Transportation', icon: Truck },
              { id: 'buffer', label: '📦 Buffer Stock', icon: Package },
              { id: 'weather', label: '☁️ Weather Data', icon: Cloud }
            ].map(item => (
              <button
                key={item.id}
                onClick={() => setCurrentPage(item.id)}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '12px',
                  margin: '8px 0',
                  background: currentPage === item.id ? '#0B5FA5' : 'transparent',
                  color: currentPage === item.id ? 'white' : textColor,
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  textAlign: 'left',
                  fontSize: '14px'
                }}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <main style={{
          flex: 1,
          padding: '30px',
          overflow: 'auto'
        }}>
          {currentPage === 'dashboard' && (
            <div>
              <h2 style={{ marginTop: 0 }}>📊 Dashboard Overview</h2>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '20px',
                marginBottom: '30px'
              }}>
                {[
                  { label: 'Current Price', value: '₹2,400/qtl', icon: '💰' },
                  { label: 'Predicted Price', value: '₹2,520/qtl', icon: '📈', trend: '+5%' },
                  { label: 'Buffer Stock', value: '3,200 MT', icon: '📦' },
                  { label: 'Risk Level', value: 'Normal', icon: '⚠️' }
                ].map((stat, idx) => (
                  <div key={idx} style={{
                    background: cardColor,
                    padding: '20px',
                    borderRadius: '12px',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
                  }}>
                    <div style={{ fontSize: '24px', marginBottom: '10px' }}>{stat.icon}</div>
                    <p style={{ margin: 0, fontSize: '12px', opacity: 0.7 }}>{stat.label}</p>
                    <p style={{ margin: '10px 0 0 0', fontSize: '20px', fontWeight: 'bold' }}>{stat.value}</p>
                    {stat.trend && <p style={{ margin: '5px 0 0 0', color: '#16A34A', fontSize: '12px' }}>{stat.trend}</p>}
                  </div>
                ))}
              </div>

              <div style={{
                background: cardColor,
                padding: '20px',
                borderRadius: '12px',
                marginBottom: '20px'
              }}>
                <h3 style={{ marginTop: 0 }}>📈 Price Trend (Last 30 Days)</h3>
                <div style={{
                  height: '200px',
                  background: darkMode ? '#0F1C2E' : '#F5F9FC',
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#999'
                }}
                >
                  📊 Chart visualization would appear here (requires Recharts installation)
                </div>
              </div>
            </div>
          )}

          {currentPage === 'forecast' && (
            <div>
              <h2 style={{ marginTop: 0 }}>🔮 Price Forecast</h2>
              <div style={{
                background: cardColor,
                padding: '20px',
                borderRadius: '12px'
              }}>
                <form style={{ display: 'grid', gap: '15px' }}>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                    <div>
                      <label>Commodity:</label>
                      <select style={{
                        width: '100%',
                        padding: '8px',
                        borderRadius: '8px',
                        border: '1px solid #DCE6EF',
                        background: bgColor,
                        color: textColor
                      }}>
                        <option>Wheat</option>
                        <option>Rice</option>
                        <option>Onion</option>
                        <option>Tomato</option>
                      </select>
                    </div>
                    <div>
                      <label>State:</label>
                      <select style={{
                        width: '100%',
                        padding: '8px',
                        borderRadius: '8px',
                        border: '1px solid #DCE6EF',
                        background: bgColor,
                        color: textColor
                      }}>
                        <option>Maharashtra</option>
                        <option>Uttar Pradesh</option>
                        <option>Punjab</option>
                      </select>
                    </div>
                  </div>
                  <div>
                    <label>Current Price (₹/qtl):</label>
                    <input
                      type="number"
                      defaultValue="2400"
                      style={{
                        width: '100%',
                        padding: '8px',
                        borderRadius: '8px',
                        border: '1px solid #DCE6EF',
                        background: bgColor,
                        color: textColor
                      }}
                    />
                  </div>
                  <button
                    type="button"
                    style={{
                      padding: '10px 20px',
                      background: '#0B5FA5',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      fontSize: '14px',
                      fontWeight: 'bold'
                    }}
                  >
                    🚀 Predict Price
                  </button>
                </form>
              </div>
            </div>
          )}

          {currentPage === 'transport' && (
            <div>
              <h2 style={{ marginTop: 0 }}>🚚 Transportation Analysis</h2>
              <div style={{
                background: cardColor,
                padding: '20px',
                borderRadius: '12px'
              }}>
                <p>Calculate transportation costs for commodity shipments</p>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '20px',
                  marginTop: '20px'
                }}>
                  <div>
                    <p>📍 Source: Nashik Warehouse</p>
                    <p>📍 Destination: Mumbai APMC</p>
                    <p>📏 Distance: 180 km</p>
                    <p>🚛 Mode: Truck</p>
                  </div>
                  <div style={{
                    background: darkMode ? '#0F1C2E' : '#F5F9FC',
                    padding: '15px',
                    borderRadius: '8px'
                  }}>
                    <p>💰 Total Cost: ₹5,400</p>
                    <p>Per KG: ₹0.54</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {currentPage === 'buffer' && (
            <div>
              <h2 style={{ marginTop: 0 }}>📦 Buffer Stock Recommendations</h2>
              <div style={{
                background: cardColor,
                padding: '20px',
                borderRadius: '12px',
                borderLeft: '5px solid #0B5FA5'
              }}>
                <h3 style={{ marginTop: 0 }}>✅ Maintain Current Stock</h3>
                <p>Current Buffer Stock: 3,200 MT</p>
                <p>Recommendation Status: Normal (Price expected to be stable)</p>
              </div>
            </div>
          )}

          {currentPage === 'weather' && (
            <div>
              <h2 style={{ marginTop: 0 }}>☁️ Weather Data</h2>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '20px'
              }}>
                {[
                  { label: '🌧️ Rainfall', value: '62 mm' },
                  { label: '🌡️ Temperature', value: '29°C' },
                  { label: '💧 Humidity', value: '58%' },
                  { label: '💨 Wind Speed', value: '12 km/h' }
                ].map((item, idx) => (
                  <div key={idx} style={{
                    background: cardColor,
                    padding: '20px',
                    borderRadius: '12px',
                    textAlign: 'center'
                  }}>
                    <p style={{ fontSize: '20px', margin: '0 0 10px 0' }}>{item.label}</p>
                    <p style={{ fontSize: '24px', fontWeight: 'bold', margin: 0 }}>{item.value}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
