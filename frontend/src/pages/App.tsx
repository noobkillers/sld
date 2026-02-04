import React from 'react';

const App: React.FC = () => {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '2rem' }}>
      <h1>SLD Reader → Digital Twin → Asset Intelligence Platform</h1>
      <p>
        Upload SLDs, create the digital twin, monitor live data, and generate
        explainable predictions without external AI APIs.
      </p>
      <section>
        <h2>Platform Modules</h2>
        <ul>
          <li>SLD ingestion and symbol/text extraction</li>
          <li>Graph-based digital twin and topology builder</li>
          <li>Multi-source data ingestion and time-series storage</li>
          <li>Rule-based intelligence and predictive maintenance</li>
          <li>Incident RCA and compliance-ready reporting</li>
        </ul>
      </section>
    </div>
  );
};

export default App;
