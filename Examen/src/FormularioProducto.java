import javax.swing.*;
import javax.swing.text.MaskFormatter;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.text.ParseException;

public class FormularioProducto extends JFrame {
    private JTextField txtNombre;
    private JTextField txtCodigo;
    private JTextField txtProveedor;
    private JTextField txtPrecioVenta;
    private JTextField txtPrecioCompra;
    private JTextField txtCategoria;
    private JFormattedTextField txtFecha;
    private JButton btnGuardar;

    public FormularioProducto() {
        initComponents();
    }

    private void initComponents() {
        setTitle("Gestión de Productos");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(400, 400);
        setLocationRelativeTo(null);

        JLabel lblNombre = new JLabel("Nombre:");
        JLabel lblCodigo = new JLabel("Código:");
        JLabel lblProveedor = new JLabel("Proveedor:");
        JLabel lblPrecioVenta = new JLabel("Precio Venta:");
        JLabel lblPrecioCompra = new JLabel("Precio Compra:");
        JLabel lblCategoria = new JLabel("Categoría:");
        JLabel lblFecha = new JLabel("Fecha (dd-MM-yyyy):");

        txtNombre = new JTextField(20);
        txtCodigo = new JTextField(20);
        txtProveedor = new JTextField(20);
        txtPrecioVenta = new JTextField(20);
        txtPrecioCompra = new JTextField(20);
        txtCategoria = new JTextField(20);

        // Crear un MaskFormatter para restringir el formato de la fecha
        MaskFormatter dateFormatter = null;
        try {
            dateFormatter = new MaskFormatter("##-##-####");
            dateFormatter.setPlaceholderCharacter('_');
        } catch (ParseException e) {
            e.printStackTrace();
        }
        txtFecha = new JFormattedTextField(dateFormatter);

        btnGuardar = new JButton("Guardar");

        // Acción del botón guardar
        btnGuardar.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                guardarProducto();
            }
        });

        // Uso de GroupLayout para mejor organización
        GroupLayout layout = new GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setAutoCreateGaps(true);
        layout.setAutoCreateContainerGaps(true);

        layout.setHorizontalGroup(
                layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                        .addGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                        .addComponent(lblNombre)
                                        .addComponent(lblCodigo)
                                        .addComponent(lblProveedor)
                                        .addComponent(lblPrecioVenta)
                                        .addComponent(lblPrecioCompra)
                                        .addComponent(lblCategoria)
                                        .addComponent(lblFecha))
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                        .addComponent(txtNombre)
                                        .addComponent(txtCodigo)
                                        .addComponent(txtProveedor)
                                        .addComponent(txtPrecioVenta)
                                        .addComponent(txtPrecioCompra)
                                        .addComponent(txtCategoria)
                                        .addComponent(txtFecha)
                                        .addComponent(btnGuardar)))
        );

        layout.setVerticalGroup(
                layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                .addComponent(lblNombre)
                                .addComponent(txtNombre))
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                .addComponent(lblCodigo)
                                .addComponent(txtCodigo))
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                .addComponent(lblProveedor)
                                .addComponent(txtProveedor))
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                .addComponent(lblPrecioVenta)
                                .addComponent(txtPrecioVenta))
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                .addComponent(lblPrecioCompra)
                                .addComponent(txtPrecioCompra))
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                .addComponent(lblCategoria)
                                .addComponent(txtCategoria))
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                .addComponent(lblFecha)
                                .addComponent(txtFecha))
                        .addComponent(btnGuardar)
        );

        pack();
    }

    private void guardarProducto() {
        String nombre = txtNombre.getText();
        String codigo = txtCodigo.getText();
        String proveedor = txtProveedor.getText();
        String precioVenta = txtPrecioVenta.getText();
        String precioCompra = txtPrecioCompra.getText();
        String categoria = txtCategoria.getText();
        String fecha = txtFecha.getText();

        // Validación básica de la fecha
        if (!fecha.matches("\\d{2}-\\d{2}-\\d{4}")) {
            JOptionPane.showMessageDialog(this, "Fecha inválida. Debe estar en el formato dd-MM-yyyy.");
            return;
        }

        // Conexión y guardado a la base de datos
        Connection conexion = ConexionDB.conectar();
        if (conexion != null) {
            try {
                String sql = "INSERT INTO productos (nombre, codigo, proveedor, precioVenta, precioCompra, categoria, fecha) VALUES (?, ?, ?, ?, ?, ?, ?)";
                PreparedStatement ps = conexion.prepareStatement(sql);
                ps.setString(1, nombre);
                ps.setString(2, codigo);
                ps.setString(3, proveedor);
                ps.setString(4, precioVenta);
                ps.setString(5, precioCompra);
                ps.setString(6, categoria);
                ps.setString(7, fecha);
                ps.executeUpdate();
                JOptionPane.showMessageDialog(this, "Producto guardado exitosamente.");

                // Limpiar campos de texto después de guardar
                limpiarCampos();
            } catch (SQLException e) {
                JOptionPane.showMessageDialog(this, "Error al guardar el producto: " + e.getMessage());
            } finally {
                try {
                    conexion.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        } else {
            JOptionPane.showMessageDialog(this, "Error en la conexión a la base de datos.");
        }
    }

    // Método para limpiar los campos de texto
    private void limpiarCampos() {
        txtNombre.setText("");
        txtCodigo.setText("");
        txtProveedor.setText("");
        txtPrecioVenta.setText("");
        txtPrecioCompra.setText("");
        txtCategoria.setText("");
        txtFecha.setValue(null);  // Limpiar el campo de fecha
    }

    public static void main(String[] args) {
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new FormularioProducto().setVisible(true);
            }
        });
    }
}
