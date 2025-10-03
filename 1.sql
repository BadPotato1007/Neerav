CREATE DATABASE  IF NOT EXISTS `runes` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `runes`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: runes
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `qno` int DEFAULT NULL,
  `sub` char(10) DEFAULT NULL,
  `question` varchar(2000) DEFAULT NULL,
  `option1` char(50) DEFAULT NULL,
  `option2` char(50) DEFAULT NULL,
  `option3` char(50) DEFAULT NULL,
  `option4` char(50) DEFAULT NULL,
  `ans` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,'Physics','A particle is moving along a straight line with initial velocity 5 m/s and acceleration 2 m/s². What is its velocity after 3 seconds?','8 m/s','9 m/s','10 m/s','11 m/s','3'),(2,'Physics','Which of the following is not a unit of energy?','Joule','Erg','Watt','Calorie','3'),(3,'Physics','The dimensional formula for pressure is:','ML⁻¹T⁻²','MLT⁻²','ML²T⁻²','M²L⁻¹T⁻²','1'),(4,'Physics','If a body is dropped from a height, its potential energy decreases and kinetic energy:','Increases','Decreases','Remains constant','Becomes zero','1'),(5,'Physics','In SHM, the acceleration is maximum when:','Velocity is maximum','Displacement is zero','Displacement is maximum','Energy is minimum','3'),(6,'Physics','A car travels first half distance with speed 60 km/h and second half with 40 km/h. The average speed is:','48 km/h','50 km/h','52 km/h','54 km/h','1'),(7,'Physics','A vector quantity among the following is:','Speed','Work','Mass','Momentum','4'),(8,'Physics','Which law states that current is directly proportional to voltage?','Faraday\'s Law','Lenz\'s Law','Ohm\'s Law','Kirchhoff\'s Law','3'),(9,'Physics','A transformer works on the principle of:','Self-induction','Mutual induction','Electrostatics','Thermodynamics','2'),(10,'Physics','Which of these is a scalar quantity?','Force','Acceleration','Velocity','Work','4'),(11,'Physics','The frequency of a wave is 50 Hz. What is its period?','0.01 s','0.02 s','0.04 s','0.05 s','4'),(12,'Physics','The speed of light in vacuum is:','3×10⁸ m/s','3×10⁶ m/s','3×10⁵ km/s','3×10⁷ m/s','1'),(13,'Physics','Which quantity is conserved in an elastic collision?','Momentum','Kinetic energy','Both','None','3'),(14,'Physics','The unit of magnetic flux is:','Tesla','Weber','Henry','Ampere','2'),(15,'Physics','Centripetal force acts in which direction?','Tangential','Outward','Inward','None','3'),(16,'Physics','1 eV is equal to:','1.6×10⁻¹⁹ J','3.2×10⁻¹⁹ J','1.6×10⁻¹⁸ J','3.2×10⁻¹⁸ J','1'),(17,'Physics','What is the SI unit of electric charge?','Coulomb','Ampere','Volt','Farad','1'),(18,'Physics','Which device converts AC to DC?','Transformer','Rectifier','Transistor','Generator','2'),(19,'Physics','A photon has:','Mass and charge','Mass only','Charge only','Neither mass nor charge','4'),(20,'Physics','The lens used in a simple microscope is:','Concave','Plano-concave','Convex','Cylindrical','3'),(21,'Physics','Escape velocity from Earth is approximately:','11.2 km/s','8.4 km/s','9.8 km/s','15 km/s','1'),(22,'Physics','The speed of sound in air is maximum in:','Winter','Summer','Rainy season','Same in all','2'),(23,'Physics','A fuse wire should have:','High resistance and high melting point','Low resistance and high melting point','High resistance and low melting point','Low resistance and low melting point','3'),(24,'Physics','Which law gives the direction of induced EMF?','Faraday\'s Law','Lenz\'s Law','Coulomb\'s Law','Ampere\'s Law','2'),(25,'Physics','SI unit of inductance is:','Weber','Tesla','Henry','Joule','3'),(26,'Physics','Which of the following is dimensionless?','Reynolds number','Power','Force','Energy','1'),(27,'Physics','Photoelectric effect supports:','Wave nature of light','Particle nature of light','Interference','Diffraction','2'),(28,'Physics','Time period of a simple pendulum is independent of:','Length','Mass','Gravity','Amplitude','2'),(29,'Physics','Which of the following is not a vector?','Acceleration','Displacement','Speed','Force','3'),(30,'Physics','Hooke’s law is related to:','Electricity','Magnetism','Elasticity','Fluids','3'),(31,'Physics','A convex mirror always forms an image which is:','Real and inverted','Real and erect','Virtual and inverted','Virtual and erect','4'),(32,'Physics','The process of heat transfer in solids is:','Radiation','Convection','Conduction','All of these','3'),(33,'Physics','Capacitance depends on:','Potential','Resistance','Area and distance between plates','Inductance','3'),(34,'Physics','Acceleration of a body moving with uniform velocity is:','0','1','2','Infinity','1'),(35,'Physics','Power is the rate of doing:','Work','Energy','Force','Mass','1'),(36,'Physics','The unit of strain is:','m','m²','m/s','Dimensionless','4'),(37,'Physics','Ohm is the SI unit of:','Voltage','Current','Resistance','Power','3'),(38,'Physics','Which of the following materials is paramagnetic?','Aluminium','Copper','Silver','Lead','1'),(39,'Physics','Which is the best conductor of electricity?','Copper','Aluminium','Silver','Gold','3'),(40,'Physics','X-rays are produced by:','Electron transitions','Nuclear fusion','Deceleration of electrons','Radioactive decay','3'),(41,'Physics','Which of the following does not affect the time period of a pendulum?','Length','Mass','Acceleration due to gravity','Amplitude','2'),(42,'Physics','Which of the following is not a fundamental force?','Gravitational','Electromagnetic','Nuclear','Frictional','4'),(43,'Physics','In resonance condition, the amplitude of oscillation is:','Minimum','Zero','Maximum','Constant','3'),(44,'Physics','Which of the following waves can travel through vacuum?','Sound','Water','Light','Seismic','3'),(45,'Physics','Which physical quantity is measured in Pascal?','Force','Energy','Pressure','Work','3'),(46,'Physics','A machine has efficiency of 80%. It means:','20% of input is wasted','80% work is wasted','All input is output','None','1'),(47,'Physics','When a magnet is cut into two, each piece has:','Only N pole','Only S pole','Both N and S poles','No poles','3'),(48,'Physics','Value of universal gravitational constant G is:','6.67×10⁻¹¹ Nm²/kg²','9.8 m/s²','3×10⁸ m/s','1.6×10⁻¹⁹ C','1'),(49,'Physics','Charge on an electron is:','+1.6×10⁻¹⁹ C','−1.6×10⁻¹⁹ C','+1.6×10⁻¹⁸ C','−1.6×10⁻¹⁸ C','2'),(50,'Physics','Transformer works on which principle?','Electrostatics','Mutual Induction','Capacitance','Self Induction','2'),(1,'Chemistry','Which one of the following has the smallest atomic radius?','Na⁺','Mg²⁺','Al³⁺','Si⁴⁺','3'),(2,'Chemistry','Which of the following molecules has a linear shape?','CO₂','H₂O','NH₃','CH₄','1'),(3,'Chemistry','Which compound gives a positive Tollen’s test?','Acetone','Formaldehyde','Acetaldehyde','Methanol','2'),(4,'Chemistry','Which of the following is a Lewis acid?','NH₃','BF₃','H₂O','CH₄','2'),(5,'Chemistry','The IUPAC name of CH₃CH₂COOH is:','Acetic acid','Propanoic acid','Formic acid','Butanoic acid','2'),(6,'Chemistry','Which of the following is an electrophile?','Cl⁻','NH₃','NO₂⁺','OH⁻','3'),(7,'Chemistry','In the periodic table, the most electropositive element is:','Sodium','Lithium','Caesium','Potassium','3'),(8,'Chemistry','Which of these has the highest bond dissociation energy?','F₂','Cl₂','Br₂','I₂','2'),(9,'Chemistry','What is the hybridization of carbon in CH₄?','sp','sp²','sp³','None','3'),(10,'Chemistry','The correct order of acidity is:','CH₃COOH > HCOOH > C₆H₅COOH','HCOOH > CH₃COOH > C₆H₅COOH','HCOOH > C₆H₅COOH > CH₃COOH','C₆H₅COOH > CH₃COOH > HCOOH','2'),(11,'Chemistry','The maximum number of electrons in a shell is given by:','2n²','n²','4n²','n','1'),(12,'Chemistry','Which among the following is an aromatic compound?','Cyclohexane','Toluene','Cyclobutane','Butene','2'),(13,'Chemistry','What is the pH of a neutral solution at 25°C?','0','7','1','14','2'),(14,'Chemistry','Which of the following is most basic?','Aniline','Methylamine','Ammonia','Phenylamine','2'),(15,'Chemistry','The oxidation number of S in H₂SO₄ is:','+4','+6','+2','+1','2'),(16,'Chemistry','Which is used as an anti-knock agent in petrol?','Methanol','Ethanol','Tetraethyl lead','Acetone','3'),(17,'Chemistry','Which pair shows the same oxidation state for Fe?','FeO and Fe₂O₃','FeO and FeCl₃','Fe₂O₃ and FeCl₃','FeSO₄ and FeCl₂','4'),(18,'Chemistry','Which one is most acidic?','Phenol','Ethanol','Acetic acid','Methanol','3'),(19,'Chemistry','What is the shape of SF₆ molecule?','Octahedral','Tetrahedral','Trigonal planar','Linear','1'),(20,'Chemistry','The bond angle in water molecule is:','109.5°','104.5°','120°','180°','2'),(21,'Chemistry','What is the main ore of aluminium?','Hematite','Bauxite','Galena','Cinnabar','2'),(22,'Chemistry','Which of the following has sp hybridization?','C₂H₂','CH₄','C₂H₄','C₂H₆','1'),(23,'Chemistry','Which gas is used in the preparation of margarine?','H₂','O₂','Cl₂','CO₂','1'),(24,'Chemistry','Which compound has peptide bond?','Glucose','Starch','Protein','Fat','3'),(25,'Chemistry','The monomer of polythene is:','C₂H₂','C₂H₄','C₃H₆','CH₄','2'),(26,'Chemistry','Which of the following is a biodegradable polymer?','Polythene','Nylon','Cellulose','PVC','3'),(27,'Chemistry','The bond order in O₂ molecule is:','1','2','3','4','3'),(28,'Chemistry','Which of these acts as a nucleophile?','H⁺','Cl⁻','BF₃','NO₂⁺','2'),(29,'Chemistry','Which of the following is not a greenhouse gas?','CO₂','CH₄','H₂O','O₂','4'),(30,'Chemistry','Which element has the highest electronegativity?','Oxygen','Nitrogen','Chlorine','Fluorine','4'),(31,'Chemistry','The chemical used for coagulation of latex is:','HCl','NH₄OH','CH₃COOH','NaOH','1'),(32,'Chemistry','Which of the following is an example of a colloid?','Sugar solution','Salt solution','Milk','Alcohol','3'),(33,'Chemistry','Which acid is present in vinegar?','Citric acid','Acetic acid','Oxalic acid','Lactic acid','2'),(34,'Chemistry','Which of these is an allotrope of carbon?','Diamond','Sand','Quartz','Chalk','1'),(35,'Chemistry','Which chemical is responsible for ozone layer depletion?','CO₂','CFCs','SO₂','CH₄','2'),(36,'Chemistry','Which of the following has a triple bond?','O₂','N₂','CO₂','NH₃','2'),(37,'Chemistry','Which is not an element of the halogen group?','F','Cl','Br','O','4'),(38,'Chemistry','Rate of a reaction depends on:','Enthalpy','Free energy','Activation energy','Temperature only','3'),(39,'Chemistry','Which element shows variable oxidation states?','Na','Al','Fe','Mg','3'),(40,'Chemistry','Which vitamin is fat-soluble?','B₁₂','C','A','B₆','3'),(41,'Chemistry','Which is a noble gas?','O₂','N₂','Ne','CO₂','3'),(42,'Chemistry','Dry ice is:','Solid CO₂','Liquid CO₂','Frozen nitrogen','Icy water','1'),(43,'Chemistry','The basicity of H₃PO₄ is:','1','2','3','4','3'),(44,'Chemistry','Which is not a strong electrolyte?','NaCl','KOH','CH₃COOH','HCl','3'),(45,'Chemistry','pH of a buffer solution remains:','Unchanged','Highly acidic','Highly basic','Very low','1'),(46,'Chemistry','The catalyst used in Haber’s process is:','Fe','Cu','Zn','Ni','1'),(47,'Chemistry','Which of these is not a greenhouse gas?','CO₂','O₃','N₂','CH₄','3'),(48,'Chemistry','Which gas is released on reaction of metals with acid?','O₂','CO₂','H₂','N₂','3'),(49,'Chemistry','Bleaching powder is chemically known as:','Ca(OH)₂','CaOCl₂','CaCO₃','CaCl₂','2'),(50,'Chemistry','Which of these elements is radioactive?','Uranium','Oxygen','Zinc','Phosphorus','1'),(1,'Maths','The roots of the equation x² - 5x + 6 = 0 are:','2 and 3','−2 and −3','1 and 6','None','1'),(2,'Maths','The value of sin(30°) is:','0','1','1/2','√3/2','3'),(3,'Maths','The derivative of x² is:','2x','x','x²','1','1'),(4,'Maths','The slope of the line y = 2x + 3 is:','2','3','1/2','−2','1'),(5,'Maths','If A = {1, 2, 3}, the number of subsets is:','3','6','8','9','3'),(6,'Maths','log₁₀(100) = ?','1','2','0','10','2'),(7,'Maths','The area of a triangle with base 5 and height 4 is:','20','9','10','8','3'),(8,'Maths','A solution of the equation x² + 4 = 0 is:','2','−2','2i','4','3'),(9,'Maths','cos(90°) = ?','0','1','−1','None','1'),(10,'Maths','If f(x) = x², then f(3) = ?','6','9','3','12','2'),(11,'Maths','If tan A = 1, then A = ?','30°','45°','60°','90°','2'),(12,'Maths','The domain of y = 1/x is:','x ≠ 1','x ≠ 0','x ≠ −1','All x','2'),(13,'Maths','The limit of (x²−1)/(x−1) as x → 1 is:','0','1','2','undefined','3'),(14,'Maths','The integral of dx/x is:','ln x + C','1/x + C','x + C','None','1'),(15,'Maths','The angle between vectors i and j is:','0°','45°','60°','90°','4'),(16,'Maths','The equation of a circle is:','x² + y² = r²','x + y = r','xy = r²','x² − y² = r²','1'),(17,'Maths','If A and B are independent, then P(A ∩ B) = ?','P(A) + P(B)','P(A) − P(B)','P(A) × P(B)','P(A) / P(B)','3'),(18,'Maths','The sum of the roots of x² − 4x + 3 = 0 is:','1','2','4','5','3'),(19,'Maths','cos²θ + sin²θ = ?','0','1','2','θ','2'),(20,'Maths','Which of the following is a quadratic equation?','x² + x + 1 = 0','x³ + x = 0','x + 1 = 0','x⁴ + 2x = 0','1'),(21,'Maths','tan(45°) = ?','0','1','√3','2','2'),(22,'Maths','The value of x in 2^x = 8 is:','2','3','4','5','2'),(23,'Maths','What is the probability of getting a 2 on a dice?','1/2','1/6','1/3','1/5','2'),(24,'Maths','The determinant of a 2x2 matrix [[a,b],[c,d]] is:','ad + bc','ab − cd','ad − bc','ac − bd','3'),(25,'Maths','The inverse of sin is denoted by:','cos⁻¹','sec','tan⁻¹','sin⁻¹','4'),(26,'Maths','The maximum value of sin x is:','0','1','2','π','2'),(27,'Maths','If A = πr², what does A represent?','Volume','Circumference','Area of a circle','None','3'),(28,'Maths','A sequence with a common ratio is called a:','AP','GP','HP','None','2'),(29,'Maths','If x³ = 27, then x = ?','9','3','2','1','2'),(30,'Maths','The number of degrees in a right angle is:','30','60','90','180','3'),(31,'Maths','The solution of sin x = 0 in [0, 2π] is:','π','0 and π','π/2','2π','2'),(32,'Maths','The sum of n natural numbers is:','n²','n(n+1)/2','n(n−1)/2','2n','2'),(33,'Maths','The mean of 2, 4, 6 is:','3','4','5','6','2'),(34,'Maths','log(ab) = ?','log a + log b','log a − log b','a log b','None','1'),(35,'Maths','If sin A = 3/5, cos A = ?','4/5','3/4','5/3','1/5','1'),(36,'Maths','A square has how many diagonals?','1','2','4','6','2'),(37,'Maths','The function y = e^x is:','Polynomial','Exponential','Trigonometric','Logarithmic','2'),(38,'Maths','Which of these is not a prime number?','2','3','4','7','3'),(39,'Maths','A rational number is:','Terminating or repeating decimal','Irrational','Imaginary','Complex','1'),(40,'Maths','The number of digits in 10^3 is:','1','2','3','4','4'),(41,'Maths','The angle of elevation is used in:','Algebra','Trigonometry','Probability','Statistics','2'),(42,'Maths','In a binomial (a + b)² = ?','a² + b²','a² + 2ab + b²','a² − 2ab + b²','2a + 2b','2'),(43,'Maths','The graph of y = x² is a:','Line','Parabola','Circle','Hyperbola','2'),(44,'Maths','The factorial of 5 is:','20','120','60','24','2'),(45,'Maths','Which of the following is a one-one function?','f(x) = x²','f(x) = x','f(x) = |x|','f(x) = sin x','2'),(46,'Maths','The value of i² is:','0','−1','1','2','2'),(47,'Maths','If two lines are perpendicular, the product of slopes is:','−1','0','1','Undefined','1'),(48,'Maths','The distance between (0,0) and (3,4) is:','5','7','4','3','1'),(49,'Maths','The function f(x) = 1/x is:','Even','Odd','Neither','Both','2'),(50,'Maths','The sum of the interior angles of a triangle is:','90°','180°','270°','360°','2');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdata`
--

DROP TABLE IF EXISTS `userdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdata` (
  `username` char(20) DEFAULT NULL,
  `email` char(30) DEFAULT NULL,
  `pass` varchar(200) DEFAULT NULL,
  `correctq` int DEFAULT '0',
  `wrongq` int DEFAULT '0',
  `totalq` int DEFAULT '0',
  `math_attempted` int DEFAULT '0',
  `phy_attempted` int DEFAULT '0',
  `chem_attempted` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdata`
--

LOCK TABLES `userdata` WRITE;
/*!40000 ALTER TABLE `userdata` DISABLE KEYS */;
INSERT INTO `userdata` VALUES ('admin','admin@runes.com','admin1234',3,5,8,1,2,5),('pranesh','kungfufighting@gmail.com','kungfufighting123',0,0,0,0,0,0),('adi','adicompc05@gmail.com','admin??',0,0,0,0,0,0),('adkfjhjk','hkjhj@lsj.com','asdhfjhdjfhd',NULL,NULL,NULL,100,0,50),('shreyas','umbini@gmail.com','shankar',NULL,NULL,NULL,100,0,50),('abc','123@gmail.com','qwe',NULL,NULL,NULL,100,0,50),('qwe','asd@r.com','qwe123',NULL,NULL,NULL,100,0,50),('qxc','a@gmail.com','zxc',NULL,NULL,NULL,0,3,0),('neerav1','neerav1@gmail.com','neerav',NULL,NULL,NULL,0,1,2),('final','final@gmail.com','final',1,3,4,1,2,1),('asd123','asd123@gmail.com','asd',1,2,3,0,2,1),('leafblower','leaf@gmail.com','happy',0,0,0,0,0,0),('leafblower','leaf@gmail.com','happy',0,0,0,0,0,0),('admin1','admin2@gmail.com','admin1',0,0,0,0,0,0),('admin','admin@gmail.com','admin1234',0,0,0,0,0,0);
/*!40000 ALTER TABLE `userdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'runes'
--

--
-- Dumping routines for database 'runes'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-03 10:06:19
