import java.sql.*;

public class Example {
    public static void main(String[] args) throws ClassNotFoundException {
        Class.forName("org.postgresql.Driver");
        String connectString = "jdbc:postgresql://flowers.mines.edu/csci403";
		System.out.print("Username: ");
		String username = System.console().readLine();
		System.out.print("Password: ");
		String password = new String(System.console().readPassword());
        Connection db;

        try {
            db = DriverManager.getConnection(connectString, username, password);
        } 
        catch (SQLException e) {
            System.out.println("Error connecting to database: " + e);
            return;
        }

        String query1 = "SELECT course_id, section, title, enrollment "
                    +   "FROM mines_courses "
                    +   "WHERE instructor = ?";


        try {
            PreparedStatement stmt = db.prepareStatement(query1);
            System.out.println("Enter an instructor: ");
            String instr = System.console().readLine();
            stmt.setString(1, instr);
            ResultSet results = stmt.executeQuery();

            while (results.next()) {
                String courseId = results.getString("course_id");
                String section = results.getString("section");
                String title = results.getString("title");
                int enrollment = results.getInt("enrollment");

                System.out.println(courseId + " " + section + " " + title + " " + enrollment);
            }
        }
        catch (SQLException e) {
            System.out.print(e);
            return;
        }


        String query2 = "UPDATE foo SET x = to_upper(x)";

        try {
            PreparedStatement stmt = db.prepareStatement(query2);
      //      stmt.setString(1, "pear");
            int rows = stmt.executeUpdate();

            System.out.println(rows + " inserted.");

        }
        catch (SQLException e) {
            System.out.print(e);
            return;
        }

    }
}
