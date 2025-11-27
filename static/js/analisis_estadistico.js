let analisisData = null;

      // Cargar análisis al iniciar
      window.addEventListener('DOMContentLoaded', function() {
        cargarAnalisis();
      });

      // Toggle secciones
      function toggleSection(sectionId) {
        const section = document.getElementById(sectionId);
        const icon = document.getElementById(sectionId + 'Icon');
        
        if (section.classList.contains('show')) {
          section.classList.remove('show');
          icon.classList.remove('fa-chevron-up');
          icon.classList.add('fa-chevron-down');
        } else {
          section.classList.add('show');
          icon.classList.remove('fa-chevron-down');
          icon.classList.add('fa-chevron-up');
        }
      }

      // Cargar análisis desde API
      async function cargarAnalisis() {
        try {
          const response = await fetch('/api/analisis-estadistico');
          const data = await response.json();
          
          if (data.error) {
            mostrarError(data.error);
            return;
          }
          
          analisisData = data.analisis;
          document.getElementById('loadingSection').style.display = 'none';
          document.getElementById('analysisContent').style.display = 'block';
          
          // Renderizar cada sección
          renderizarNormal();
          renderizarBinomial();
          renderizarPoisson();
          renderizarEsperanza();
          renderizarBayes();
          renderizarIntervalos();
          renderizarHipotesis();
          
        } catch (error) {
          mostrarError('Error al cargar el análisis: ' + error.message);
        }
      }

      function mostrarError(mensaje) {
        document.getElementById('loadingSection').style.display = 'none';
        document.getElementById('errorSection').style.display = 'block';
        document.getElementById('errorMessage').textContent = mensaje;
      }

      // Renderizar Distribución Normal
      function renderizarNormal() {
        const pasos = analisisData.distribucion_normal;
        let html = '';
        
        pasos.forEach((paso, index) => {
          html += `<div class="step-card">`;
          html += `<h5><span class="step-number">${index + 1}</span>${paso.titulo}</h5>`;
          
          if (paso.descripcion) {
            html += `<p class="text-muted">${paso.descripcion}</p>`;
          }
          
          if (paso.formula) {
            html += `<div class="formula-box">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.formula_desarrollada) {
              html += `<div class="formula descripcion mt-2">${paso.formula_desarrollada}</div>`;
            }
            html += `</div>`;
          }
          
          // Variables
          if (paso.variables) {
            html += `<div class="mt-3"><strong>Variables:</strong>`;
            Object.keys(paso.variables).forEach(key => {
              html += `<div class="variable-item"><strong>${key}:</strong> ${paso.variables[key]}</div>`;
            });
            html += `</div>`;
          }
          
          // Medidas centrales y dispersión
          if (paso.medidas_centrales) {
            html += `<div class="mt-3"><strong>Medidas de Tendencia Central:</strong>`;
            Object.keys(paso.medidas_centrales).forEach(key => {
              const valor = paso.medidas_centrales[key];
              const formateado = typeof valor === 'number' && key.toLowerCase().includes('precio') ? 
                `$${valor.toLocaleString('es-ES', {minimumFractionDigits: 2, maximumFractionDigits: 2})}` : 
                typeof valor === 'number' ? valor.toLocaleString('es-ES') : valor;
              html += `<div class="variable-item"><strong>${key}:</strong> ${formateado}</div>`;
            });
            html += `</div>`;
          }
          
          if (paso.medidas_dispersion) {
            html += `<div class="mt-3"><strong>Medidas de Dispersión:</strong>`;
            Object.keys(paso.medidas_dispersion).forEach(key => {
              const valor = paso.medidas_dispersion[key];
              const formateado = typeof valor === 'number' ? valor.toLocaleString('es-ES') : valor;
              html += `<div class="variable-item"><strong>${key}:</strong> ${formateado}</div>`;
            });
            html += `</div>`;
          }
          
          // Parámetros
          if (paso.parametros) {
            html += `<div class="mt-3"><strong>Parámetros:</strong>`;
            Object.keys(paso.parametros).forEach(key => {
              const valor = paso.parametros[key];
              const formateado = typeof valor === 'number' ? valor.toLocaleString('es-ES') : valor;
              html += `<div class="variable-item"><strong>${key}:</strong> ${formateado}</div>`;
            });
            html += `</div>`;
          }
          
          // Test de normalidad
          if (paso.estadistico !== undefined) {
            html += `<div class="mt-3">`;
            html += `<strong>Test de Normalidad (Shapiro-Wilk):</strong>`;
            html += `<div class="variable-item"><strong>Estadístico:</strong> ${paso.estadistico.toFixed(6)}</div>`;
            html += `<div class="variable-item"><strong>P-valor:</strong> ${paso.p_valor.toFixed(6)}</div>`;
            html += `<div class="variable-item"><strong>Nivel de significancia:</strong> ${paso.nivel_significancia || 0.05}</div>`;
            if (paso.conclusion) {
              html += `<div class="conclusion mt-2"><strong>Conclusión:</strong> ${paso.conclusion}</div>`;
            }
            html += `</div>`;
          }
          
          // Regla empírica
          if (paso.regla_empirica) {
            html += `<div class="mt-3"><strong>Regla Empírica (68-95-99.7%):</strong>`;
            Object.keys(paso.regla_empirica).forEach(key => {
              html += `<div class="variable-item"><strong>${key}:</strong> ${paso.regla_empirica[key]}</div>`;
            });
            html += `</div>`;
          }
          
          if (paso.interpretacion) {
            html += `<div class="interpretacion mt-3"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
          }
          
          html += `</div>`;
        });
        
        document.getElementById('normalSection').innerHTML = html;
      }

      // Renderizar Distribución Binomial
      function renderizarBinomial() {
        const pasos = analisisData.distribucion_binomial;
        let html = '';
        
        pasos.forEach((paso, index) => {
          html += `<div class="step-card">`;
          html += `<h5><span class="step-number">${index + 1}</span>${paso.titulo}</h5>`;
          
          if (paso.descripcion) {
            html += `<p class="text-muted">${paso.descripcion}</p>`;
          }
          
          if (paso.formula) {
            html += `<div class="formula-box">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.formula_desarrollada) {
              html += `<div class="formula descripcion mt-2">${paso.formula_desarrollada}</div>`;
            }
            html += `</div>`;
          }
          
          // Variables
          if (paso.variables) {
            html += `<div class="mt-3"><strong>Variables:</strong>`;
            Object.keys(paso.variables).forEach(key => {
              html += `<div class="variable-item"><strong>${key}:</strong> ${paso.variables[key]}</div>`;
            });
            html += `</div>`;
          }
          
          // Valores
          if (paso.valores) {
            html += `<div class="mt-3"><strong>Valores:</strong>`;
            Object.keys(paso.valores).forEach(key => {
              const valor = paso.valores[key];
              const formateado = typeof valor === 'number' ? valor.toFixed(4) : valor;
              html += `<div class="variable-item"><strong>${key}:</strong> ${formateado}</div>`;
            });
            html += `</div>`;
          }
          
          // PMF valores
          if (paso.pmf_valores) {
            html += `<div class="mt-3"><strong>Función de Masa de Probabilidad (PMF):</strong>`;
            Object.keys(paso.pmf_valores).forEach(key => {
              html += `<div class="variable-item"><strong>${key}:</strong> ${paso.pmf_valores[key].toFixed(4)}</div>`;
            });
            html += `</div>`;
          }
          
          // Fórmulas de esperanza y varianza
          if (paso.esperanza_formula) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.esperanza_formula}</div>`;
            if (paso.esperanza_calculo) {
              html += `<div class="formula descripcion mt-2">${paso.esperanza_calculo}</div>`;
            }
            if (paso.esperanza_valor !== undefined) {
              html += `<div class="variable-item mt-2"><strong>Resultado:</strong> ${paso.esperanza_valor.toFixed(4)}</div>`;
            }
            html += `</div>`;
          }
          
          if (paso.varianza_formula) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.varianza_formula}</div>`;
            if (paso.varianza_calculo) {
              html += `<div class="formula descripcion mt-2">${paso.varianza_calculo}</div>`;
            }
            if (paso.varianza_valor !== undefined) {
              html += `<div class="variable-item mt-2"><strong>Resultado:</strong> ${paso.varianza_valor.toFixed(6)}</div>`;
            }
            html += `</div>`;
          }
          
          // PMF simulación
          if (paso.pmf_simulacion) {
            html += `<div class="mt-3"><strong>PMF para n=${paso.pmf_simulacion.length - 1} viviendas:</strong>`;
            html += `<div class="table-responsive mt-2">`;
            html += `<table class="table table-sm">`;
            html += `<thead><tr><th>k</th><th>P(S = k)</th></tr></thead>`;
            html += `<tbody>`;
            paso.pmf_simulacion.forEach(item => {
              html += `<tr><td>${item.k}</td><td>${item.probabilidad.toFixed(4)}</td></tr>`;
            });
            html += `</tbody></table></div></div>`;
          }
          
          if (paso.interpretacion) {
            html += `<div class="interpretacion mt-3"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
          }
          
          html += `</div>`;
        });
        
        document.getElementById('binomialSection').innerHTML = html;
      }

      // Renderizar Distribución Poisson
      function renderizarPoisson() {
        const pasos = analisisData.distribucion_poisson;
        let html = '';
        
        pasos.forEach((paso, index) => {
          html += `<div class="step-card">`;
          html += `<h5><span class="step-number">${index + 1}</span>${paso.titulo}</h5>`;
          
          if (paso.descripcion) {
            html += `<p class="text-muted">${paso.descripcion}</p>`;
          }
          
          if (paso.formula) {
            html += `<div class="formula-box">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.formula_desarrollada) {
              html += `<div class="formula descripcion mt-2">${paso.formula_desarrollada}</div>`;
            }
            html += `</div>`;
          }
          
          // Variables
          if (paso.variables) {
            html += `<div class="mt-3"><strong>Variables:</strong>`;
            Object.keys(paso.variables).forEach(key => {
              html += `<div class="variable-item"><strong>${key}:</strong> ${paso.variables[key]}</div>`;
            });
            html += `</div>`;
          }
          
          // Parámetro
          if (paso.parametro) {
            html += `<div class="mt-3"><strong>Parámetro λ:</strong>`;
            Object.keys(paso.parametro).forEach(key => {
              const valor = paso.parametro[key];
              const formateado = typeof valor === 'number' ? valor.toFixed(4) : valor;
              html += `<div class="variable-item"><strong>${key}:</strong> ${formateado}</div>`;
            });
            html += `</div>`;
          }
          
          // PMF ejemplos
          if (paso.pmf_ejemplos) {
            html += `<div class="mt-3"><strong>Ejemplos de PMF:</strong>`;
            paso.pmf_ejemplos.forEach(ejemplo => {
              html += `<div class="formula-box mt-2">`;
              html += `<div class="formula">${ejemplo.formula}</div>`;
              if (ejemplo.calculo) {
                html += `<div class="formula descripcion mt-2">${ejemplo.calculo}</div>`;
              }
              html += `<div class="variable-item mt-2"><strong>P(Z = ${ejemplo.k}):</strong> ${ejemplo.valor.toFixed(4)}</div>`;
              html += `</div>`;
            });
            html += `</div>`;
          }
          
          // Comparación observada vs teórica
          if (paso.tabla_comparacion) {
            html += `<div class="mt-3"><strong>Comparación Observada vs Teórica:</strong>`;
            html += `<div class="table-responsive mt-2">`;
            html += `<table class="table table-sm">`;
            html += `<thead><tr><th>k</th><th>Frec. Observada</th><th>Frec. Esperada</th><th>P(Z=k)</th></tr></thead>`;
            html += `<tbody>`;
            paso.tabla_comparacion.forEach(item => {
              html += `<tr>`;
              html += `<td>${item.k}</td>`;
              html += `<td>${item.frec_observada}</td>`;
              html += `<td>${item.frec_esperada.toFixed(2)}</td>`;
              html += `<td>${item.probabilidad_teorica.toFixed(4)}</td>`;
              html += `</tr>`;
            });
            html += `</tbody></table></div></div>`;
          }
          
          // Esperanza y varianza
          if (paso.esperanza_formula) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.esperanza_formula}</div>`;
            html += `<div class="variable-item mt-2"><strong>E(Z):</strong> ${paso.esperanza_valor.toFixed(4)}</div>`;
            html += `</div>`;
          }
          
          if (paso.varianza_formula) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.varianza_formula}</div>`;
            if (paso.propiedad) {
              html += `<div class="formula descripcion mt-2"><strong>Propiedad especial:</strong> ${paso.propiedad}</div>`;
            }
            html += `<div class="variable-item mt-2"><strong>Var(Z):</strong> ${paso.varianza_valor.toFixed(4)}</div>`;
            html += `</div>`;
          }
          
          // Condiciones
          if (paso.condiciones) {
            html += `<div class="mt-3"><strong>Condiciones para usar Poisson:</strong>`;
            Object.keys(paso.condiciones).forEach(key => {
              html += `<div class="variable-item"><strong>${key}:</strong> ${paso.condiciones[key]}</div>`;
            });
            if (paso.cumple_condiciones !== undefined) {
              const estado = paso.cumple_condiciones ? '✅ Sí' : '❌ No';
              html += `<div class="variable-item mt-2"><strong>Cumple condiciones:</strong> ${estado}</div>`;
            }
            html += `</div>`;
          }
          
          if (paso.interpretacion) {
            html += `<div class="interpretacion mt-3"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
          }
          
          html += `</div>`;
        });
        
        document.getElementById('poissonSection').innerHTML = html;
      }

      // Renderizar Esperanza y Varianza
      function renderizarEsperanza() {
        const pasos = analisisData.esperanza_varianza;
        let html = '';
        
        pasos.forEach((paso, index) => {
          html += `<div class="step-card">`;
          html += `<h5><span class="step-number">${index + 1}</span>${paso.titulo}</h5>`;
          
          if (paso.descripcion) {
            html += `<p class="text-muted">${paso.descripcion}</p>`;
          }
          
          // Fórmulas
          if (paso.formula_continua || paso.formula_discreta || paso.formula_empirica) {
            html += `<div class="formula-box">`;
            if (paso.formula_continua) {
              html += `<div class="formula">${paso.formula_continua}</div>`;
            }
            if (paso.formula_discreta) {
              html += `<div class="formula">${paso.formula_discreta}</div>`;
            }
            if (paso.formula_empirica) {
              html += `<div class="formula">${paso.formula_empirica}</div>`;
            }
            if (paso.formula_calculo) {
              html += `<div class="formula descripcion mt-2">${paso.formula_calculo}</div>`;
            }
            if (paso.valor !== undefined) {
              const formateado = typeof paso.valor === 'number' && paso.titulo.toLowerCase().includes('esperanza') ? 
                `$${paso.valor.toLocaleString('es-ES', {minimumFractionDigits: 2, maximumFractionDigits: 2})}` : 
                typeof paso.valor === 'number' ? paso.valor.toLocaleString('es-ES') : paso.valor;
              html += `<div class="variable-item mt-2"><strong>Valor:</strong> ${formateado}</div>`;
            }
            html += `</div>`;
          }
          
          // Valores (para esperanza condicional)
          if (paso.valores) {
            html += `<div class="mt-3"><strong>Valores:</strong>`;
            Object.keys(paso.valores).forEach(key => {
              const valor = paso.valores[key];
              const formateado = typeof valor === 'number' ? 
                `$${valor.toLocaleString('es-ES', {minimumFractionDigits: 2, maximumFractionDigits: 2})}` : 
                valor;
              html += `<div class="variable-item"><strong>${key}:</strong> ${formateado}</div>`;
            });
            if (paso.n_con_lago) {
              html += `<div class="variable-item"><strong>N con lago:</strong> ${paso.n_con_lago}</div>`;
            }
            if (paso.n_sin_lago) {
              html += `<div class="variable-item"><strong>N sin lago:</strong> ${paso.n_sin_lago}</div>`;
            }
            html += `</div>`;
          }
          
          // Propiedades
          if (paso.propiedad_1) {
            html += `<div class="mt-3"><strong>Propiedades Matemáticas:</strong>`;
            html += `<div class="variable-item">${paso.propiedad_1}</div>`;
            if (paso.propiedad_2) html += `<div class="variable-item">${paso.propiedad_2}</div>`;
            if (paso.propiedad_3) html += `<div class="variable-item">${paso.propiedad_3}</div>`;
            if (paso.propiedad_4) html += `<div class="variable-item">${paso.propiedad_4}</div>`;
            html += `</div>`;
          }
          
          // Coeficiente de variación
          if (paso.valor !== undefined && paso.titulo && paso.titulo.includes('Coeficiente')) {
            html += `<div class="formula-box mt-3">`;
            if (paso.formula) {
              html += `<div class="formula">${paso.formula}</div>`;
            }
            if (paso.formula_calculo) {
              html += `<div class="formula descripcion mt-2">${paso.formula_calculo}</div>`;
            }
            html += `<div class="variable-item mt-2"><strong>CV:</strong> ${paso.valor.toFixed(2)}%</div>`;
            html += `</div>`;
          }
          
          if (paso.interpretacion) {
            html += `<div class="interpretacion mt-3"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
          }
          
          html += `</div>`;
        });
        
        document.getElementById('esperanzaSection').innerHTML = html;
      }

      // Renderizar Teorema de Bayes
      function renderizarBayes() {
        const pasos = analisisData.teorema_bayes;
        let html = '';
        
        pasos.forEach((paso, index) => {
          html += `<div class="step-card">`;
          html += `<h5><span class="step-number">${index + 1}</span>${paso.titulo}</h5>`;
          
          if (paso.descripcion) {
            html += `<p class="text-muted">${paso.descripcion}</p>`;
          }
          
          // Eventos
          if (paso.eventos) {
            html += `<div class="mt-3"><strong>Eventos:</strong>`;
            Object.keys(paso.eventos).forEach(key => {
              html += `<div class="variable-item"><strong>${key}:</strong> ${paso.eventos[key]}</div>`;
            });
            html += `</div>`;
          }
          
          // Conteos
          if (paso.conteos) {
            html += `<div class="mt-3"><strong>Conteos de la Muestra:</strong>`;
            Object.keys(paso.conteos).forEach(key => {
              html += `<div class="variable-item"><strong>${key}:</strong> ${paso.conteos[key].toLocaleString('es-ES')}</div>`;
            });
            html += `</div>`;
          }
          
          // Probabilidades con cálculos
          if (paso.formula_pa) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula_pa}</div>`;
            if (paso.calculo_pa) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_pa}</div>`;
            }
            if (paso.valor_pa !== undefined) {
              html += `<div class="variable-item mt-2"><strong>P(A):</strong> ${paso.valor_pa.toFixed(4)} (${(paso.valor_pa*100).toFixed(2)}%)</div>`;
            }
            html += `</div>`;
          }
          
          if (paso.formula_pb) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula_pb}</div>`;
            if (paso.calculo_pb) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_pb}</div>`;
            }
            if (paso.valor_pb !== undefined) {
              html += `<div class="variable-item mt-2"><strong>P(B):</strong> ${paso.valor_pb.toFixed(4)} (${(paso.valor_pb*100).toFixed(2)}%)</div>`;
            }
            html += `</div>`;
          }
          
          // Probabilidades condicionales
          if (paso.formula_condicional) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula_condicional}</div>`;
            if (paso.calculo_pa_dado_b) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_pa_dado_b}</div>`;
            }
            if (paso.valor_pa_dado_b !== undefined) {
              html += `<div class="variable-item mt-2"><strong>P(A|B):</strong> ${paso.valor_pa_dado_b.toFixed(4)} (${(paso.valor_pa_dado_b*100).toFixed(2)}%)</div>`;
            }
            html += `</div>`;
          }
          
          // Teorema de Bayes
          if (paso.formula && paso.titulo && paso.titulo.includes('Bayes')) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.formula_nombres) {
              html += `<div class="formula descripcion mt-2"><strong>${paso.formula_nombres}</strong></div>`;
            }
            if (paso.calculo_paso1) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_paso1}</div>`;
            }
            if (paso.calculo_paso2) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_paso2}</div>`;
            }
            
            // Componentes
            if (paso.componentes) {
              html += `<div class="mt-3"><strong>Componentes del Teorema:</strong>`;
              Object.keys(paso.componentes).forEach(key => {
                html += `<div class="variable-item"><strong>${key}:</strong> ${paso.componentes[key].toFixed(4)}</div>`;
              });
              html += `</div>`;
            }
            html += `</div>`;
          }
          
          // Interpretación con incremento
          if (paso.probabilidad_antes && paso.probabilidad_despues) {
            html += `<div class="mt-3">`;
            html += `<div class="variable-item"><strong>Probabilidad antes (P(A)):</strong> ${(paso.probabilidad_antes.valor*100).toFixed(2)}%</div>`;
            html += `<div class="variable-item"><strong>Probabilidad después (P(A|B)):</strong> ${(paso.probabilidad_despues.valor*100).toFixed(2)}%</div>`;
            if (paso.incremento) {
              html += `<div class="conclusion mt-2">`;
              html += `<strong>Incremento:</strong> +${paso.incremento.porcentual.toFixed(2)} puntos porcentuales `;
              html += `(factor de ${paso.incremento.factor.toFixed(2)}x)`;
              html += `</div>`;
            }
            html += `</div>`;
          }
          
          if (paso.interpretacion) {
            html += `<div class="interpretacion mt-3"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
          }
          
          if (paso.interpretacion_final) {
            html += `<div class="conclusion mt-3"><strong>Conclusión:</strong> ${paso.interpretacion_final}</div>`;
          }
          
          html += `</div>`;
        });
        
        document.getElementById('bayesSection').innerHTML = html;
      }

      // Renderizar Intervalos de Confianza
      function renderizarIntervalos() {
        const pasos = analisisData.intervalos_confianza;
        let html = '';
        
        pasos.forEach((paso, index) => {
          html += `<div class="step-card">`;
          html += `<h5><span class="step-number">${index + 1}</span>${paso.titulo}</h5>`;
          
          if (paso.descripcion) {
            html += `<p class="text-muted">${paso.descripcion}</p>`;
          }
          
          // Objetivo
          if (paso.formula_objetivo) {
            html += `<div class="formula-box">`;
            html += `<div class="formula">${paso.formula_objetivo}</div>`;
            html += `</div>`;
          }
          
          // Parámetros
          if (paso.parametros) {
            html += `<div class="mt-3"><strong>Parámetros:</strong>`;
            Object.keys(paso.parametros).forEach(key => {
              const valor = paso.parametros[key];
              const formateado = typeof valor === 'number' ? 
                (key.includes('%') ? `${(valor*100).toFixed(0)}%` : valor.toFixed(4)) : 
                valor;
              html += `<div class="variable-item"><strong>${key}:</strong> ${formateado}</div>`;
            });
            html += `</div>`;
          }
          
          // Valores de la muestra
          if (paso.valores) {
            html += `<div class="mt-3"><strong>Estadísticas de la Muestra:</strong>`;
            Object.keys(paso.valores).forEach(key => {
              const valor = paso.valores[key];
              const formateado = typeof valor === 'number' && key.toLowerCase().includes('media') ? 
                `$${valor.toLocaleString('es-ES', {minimumFractionDigits: 2, maximumFractionDigits: 2})}` : 
                typeof valor === 'number' ? valor.toLocaleString('es-ES') : valor;
              html += `<div class="variable-item"><strong>${key}:</strong> ${formateado}</div>`;
            });
            html += `</div>`;
          }
          
          // Error estándar
          if (paso.formula_error_estandar) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula_error_estandar}</div>`;
            if (paso.calculo_error_estandar) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_error_estandar}</div>`;
            }
            if (paso.error_estandar !== undefined) {
              html += `<div class="variable-item mt-2"><strong>Error estándar (SE):</strong> $${paso.error_estandar.toLocaleString('es-ES', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>`;
            }
            html += `</div>`;
          }
          
          // Valor crítico t
          if (paso.formula) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.busqueda) {
              html += `<div class="formula descripcion mt-2">${paso.busqueda}</div>`;
            }
            if (paso.formula_calculo) {
              html += `<div class="formula descripcion mt-2">${paso.formula_calculo}</div>`;
            }
            if (paso.valor_critico !== undefined) {
              html += `<div class="variable-item mt-2"><strong>t crítico:</strong> ${paso.valor_critico.toFixed(4)}</div>`;
            }
            html += `</div>`;
          }
          
          // Margen de error
          if (paso.formula && paso.titulo && paso.titulo.includes('Margen')) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.calculo_paso1) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_paso1}</div>`;
            }
            if (paso.calculo_paso2) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_paso2}</div>`;
            }
            if (paso.calculo_paso3) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_paso3}</div>`;
            }
            if (paso.margen_error !== undefined) {
              html += `<div class="variable-item mt-2"><strong>Margen de error:</strong> $${paso.margen_error.toLocaleString('es-ES', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>`;
            }
            html += `</div>`;
          }
          
          // Intervalo final
          if (paso.intervalo) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula_final || paso.formula}</div>`;
            if (paso.calculo_inferior) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_inferior}</div>`;
            }
            if (paso.calculo_superior) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_superior}</div>`;
            }
            html += `<div class="mt-3"><strong>Intervalo de Confianza:</strong>`;
            html += `<div class="variable-item"><strong>Límite inferior:</strong> $${paso.intervalo['Límite inferior'].toLocaleString('es-ES', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>`;
            html += `<div class="variable-item"><strong>Límite superior:</strong> $${paso.intervalo['Límite superior'].toLocaleString('es-ES', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>`;
            html += `<div class="variable-item"><strong>Amplitud:</strong> $${paso.intervalo.Amplitud.toLocaleString('es-ES', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>`;
            html += `</div>`;
            html += `</div>`;
          }
          
          // Comparación de niveles
          if (paso.comparacion) {
            html += `<div class="mt-3"><strong>Comparación de Diferentes Niveles de Confianza:</strong>`;
            html += `<div class="table-responsive mt-2">`;
            html += `<table class="table table-sm">`;
            html += `<thead><tr><th>Nivel</th><th>t crítico</th><th>Margen Error</th><th>Límite Inf.</th><th>Límite Sup.</th><th>Amplitud</th></tr></thead>`;
            html += `<tbody>`;
            paso.comparacion.forEach(item => {
              html += `<tr>`;
              html += `<td>${item.nivel}%</td>`;
              html += `<td>${item.t_critico.toFixed(4)}</td>`;
              html += `<td>$${item.margen_error.toFixed(2)}</td>`;
              html += `<td>$${item.inferior.toFixed(2)}</td>`;
              html += `<td>$${item.superior.toFixed(2)}</td>`;
              html += `<td>$${item.amplitud.toFixed(2)}</td>`;
              html += `</tr>`;
            });
            html += `</tbody></table></div>`;
            if (paso.observacion) {
              html += `<div class="interpretacion mt-2"><strong>Observación:</strong> ${paso.observacion}</div>`;
            }
            html += `</div>`;
          }
          
          if (paso.interpretacion) {
            html += `<div class="interpretacion mt-3"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
          }
          
          html += `</div>`;
        });
        
        document.getElementById('intervalosSection').innerHTML = html;
      }

      // Renderizar Pruebas de Hipótesis
      function renderizarHipotesis() {
        const pasos = analisisData.pruebas_hipotesis;
        let html = '';
        
        pasos.forEach((prueba, index) => {
          html += `<div class="step-card" style="border-left-color: ${index === 0 ? '#f59e0b' : '#8b5cf6'}; margin-bottom: 2rem;">`;
          html += `<h5 style="color: ${index === 0 ? '#f59e0b' : '#8b5cf6'};">${prueba.titulo}</h5>`;
          
          if (prueba.descripcion) {
            html += `<p class="text-muted">${prueba.descripcion}</p>`;
          }
          
          // Paso 1: Hipótesis
          if (prueba.paso_1_hipotesis) {
            const paso = prueba.paso_1_hipotesis;
            html += `<div class="mt-3"><strong>${paso.titulo}:</strong>`;
            html += `<div class="variable-item"><strong>H₀:</strong> ${paso.h0}</div>`;
            html += `<div class="variable-item"><strong>H₁:</strong> ${paso.h1}</div>`;
            if (paso.tipo_prueba) {
              html += `<div class="variable-item"><strong>Tipo de prueba:</strong> ${paso.tipo_prueba}</div>`;
            }
            if (paso.nivel_significancia) {
              html += `<div class="variable-item"><strong>Nivel de significancia:</strong> ${paso.nivel_significancia}</div>`;
            }
            html += `</div>`;
          }
          
          // Paso 2: Datos
          if (prueba.paso_2_datos) {
            const paso = prueba.paso_2_datos;
            html += `<div class="mt-3"><strong>${paso.titulo}:</strong>`;
            if (paso.muestra_1) {
              html += `<div class="variable-item"><strong>${paso.muestra_1.nombre}:</strong> n=${paso.muestra_1.n}, x̄=$${paso.muestra_1.media.toLocaleString('es-ES', {minimumFractionDigits: 2})}, s=$${paso.muestra_1.desviacion.toLocaleString('es-ES', {minimumFractionDigits: 2})}</div>`;
            }
            if (paso.muestra_2) {
              html += `<div class="variable-item"><strong>${paso.muestra_2.nombre}:</strong> n=${paso.muestra_2.n}, x̄=$${paso.muestra_2.media.toLocaleString('es-ES', {minimumFractionDigits: 2})}, s=$${paso.muestra_2.desviacion.toLocaleString('es-ES', {minimumFractionDigits: 2})}</div>`;
            }
            if (paso.diferencia !== undefined) {
              html += `<div class="variable-item"><strong>Diferencia:</strong> $${paso.diferencia.toLocaleString('es-ES', {minimumFractionDigits: 2})}</div>`;
            }
            html += `</div>`;
          }
          
          // Paso 3: Estadístico
          if (prueba.paso_3_estadistico) {
            const paso = prueba.paso_3_estadistico;
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.formula_se) {
              html += `<div class="formula descripcion mt-2">${paso.formula_se}</div>`;
            }
            if (paso.calculo_se) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_se}</div>`;
            }
            if (paso.se_valor !== undefined) {
              html += `<div class="variable-item mt-2"><strong>Error estándar (SE):</strong> ${paso.se_valor.toFixed(2)}</div>`;
            }
            if (paso.calculo_t) {
              html += `<div class="formula descripcion mt-2">${paso.calculo_t}</div>`;
            }
            if (paso.t_estadistico !== undefined) {
              html += `<div class="variable-item mt-2"><strong>Estadístico t:</strong> ${paso.t_estadistico.toFixed(4)}</div>`;
            }
            if (paso.df_aproximado) {
              html += `<div class="variable-item"><strong>Grados de libertad (df):</strong> ${paso.df_aproximado}</div>`;
            }
            html += `</div>`;
          }
          
          // Paso 4: P-valor
          if (prueba.paso_4_pvalor) {
            const paso = prueba.paso_4_pvalor;
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.p_valor !== undefined) {
              html += `<div class="variable-item mt-2"><strong>P-valor:</strong> ${paso.p_valor.toFixed(6)}</div>`;
            }
            if (paso.interpretacion_p) {
              html += `<div class="interpretacion mt-2"><strong>Nota:</strong> ${paso.interpretacion_p}</div>`;
            }
            html += `</div>`;
          }
          
          // Paso 5: Conclusión (test t)
          if (prueba.paso_5_conclusion) {
            const paso = prueba.paso_5_conclusion;
            html += `<div class="mt-3"><strong>${paso.titulo}:</strong>`;
            html += `<div class="variable-item"><strong>Regla de decisión:</strong> ${paso.regla_decision}</div>`;
            html += `<div class="variable-item"><strong>Comparación:</strong> ${paso.comparacion}</div>`;
            html += `<div class="conclusion mt-2">`;
            html += `<strong>Decisión:</strong> ${paso.decision}<br>`;
            html += `<strong>Conclusión:</strong> ${paso.conclusion}`;
            html += `</div>`;
            html += `</div>`;
          }
          
          // Tabla de contingencia (Chi-cuadrado)
          if (prueba.paso_2_tabla_observada) {
            const paso = prueba.paso_2_tabla_observada;
            html += `<div class="mt-3"><strong>${paso.titulo}:</strong>`;
            if (paso.tabla) {
              html += `<div class="table-responsive mt-2">`;
              html += `<table class="table table-sm">`;
              html += `<thead><tr><th></th>`;
              Object.keys(paso.tabla).forEach(col => {
                html += `<th>${col}</th>`;
              });
              html += `</tr></thead><tbody>`;
              Object.keys(paso.tabla).forEach(fila => {
                html += `<tr><th>${fila}</th>`;
                Object.values(paso.tabla[fila]).forEach(valor => {
                  html += `<td>${valor}</td>`;
                });
                html += `</tr>`;
              });
              html += `</tbody></table></div>`;
            }
            if (paso.totales) {
              html += `<div class="mt-2"><strong>Totales:</strong>`;
              if (paso.totales['Total por fila']) {
                Object.keys(paso.totales['Total por fila']).forEach(key => {
                  html += `<div class="variable-item"><strong>${key}:</strong> ${paso.totales['Total por fila'][key]}</div>`;
                });
              }
              html += `</div>`;
            }
            html += `</div>`;
          }
          
          // Estadístico Chi-cuadrado
          if (prueba.paso_4_estadistico) {
            const paso = prueba.paso_4_estadistico;
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.chi2_estadistico !== undefined) {
              html += `<div class="variable-item mt-2"><strong>Estadístico χ²:</strong> ${paso.chi2_estadistico.toFixed(4)}</div>`;
            }
            if (paso.grados_libertad) {
              html += `<div class="variable-item"><strong>Grados de libertad:</strong> ${paso.grados_libertad}</div>`;
            }
            html += `</div>`;
          }
          
          // P-valor Chi-cuadrado
          if (prueba.paso_5_pvalor) {
            const paso = prueba.paso_5_pvalor;
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.p_valor !== undefined) {
              html += `<div class="variable-item mt-2"><strong>P-valor:</strong> ${paso.p_valor.toFixed(6)}</div>`;
            }
            if (paso.chi2_critico !== undefined) {
              html += `<div class="variable-item"><strong>χ² crítico (α=0.05):</strong> ${paso.chi2_critico.toFixed(4)}</div>`;
            }
            html += `</div>`;
          }
          
          // Conclusión Chi-cuadrado
          if (prueba.paso_6_conclusion) {
            const paso = prueba.paso_6_conclusion;
            html += `<div class="mt-3"><strong>${paso.titulo}:</strong>`;
            html += `<div class="variable-item"><strong>Regla de decisión:</strong> ${paso.regla_decision}</div>`;
            html += `<div class="variable-item"><strong>Comparación:</strong> ${paso.comparacion}</div>`;
            html += `<div class="conclusion mt-2">`;
            html += `<strong>Decisión:</strong> ${paso.decision}<br>`;
            html += `<strong>Conclusión:</strong> ${paso.conclusion}`;
            html += `</div>`;
            html += `</div>`;
          }
          
          html += `</div>`;
        });
        
        document.getElementById('hipotesisSection').innerHTML = html;
      }
